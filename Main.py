import tkinter as tk
from tkinter import ttk, messagebox

from modules import (
    load_records, add_record, update_record, delete_record, get_summary,
    search_records, sort_records, VALID_STATUSES,
)


class IPManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IP Management Tool")
        self.geometry("1080x700")
        self.minsize(900, 580)
        self.configure(bg="#0d1117")
        self.resizable(True, True)

        self.records = load_records()
        self._sort_col = "ip"
        self._sort_rev = False

        self._build_styles()
        self._build_ui()
        self._refresh_table()

    # ── styles ────────────────────────────────────────────────────────────────

    def _build_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("T.Treeview",
            background="#161b22", foreground="#c9d1d9",
            fieldbackground="#161b22", rowheight=34,
            font=("Consolas", 11), borderwidth=0)
        s.configure("T.Treeview.Heading",
            background="#21262d", foreground="#58a6ff",
            font=("Consolas", 11, "bold"), relief="flat", borderwidth=0)
        s.map("T.Treeview",
            background=[("selected", "#1f6feb")],
            foreground=[("selected", "#ffffff")])
        s.map("T.Treeview.Heading",
            background=[("active", "#30363d")])
        s.configure("T.Vertical.TScrollbar",
            background="#21262d", troughcolor="#161b22",
            arrowcolor="#58a6ff", borderwidth=0)

    # ── top bar ───────────────────────────────────────────────────────────────

    def _build_ui(self):
        topbar = tk.Frame(self, bg="#161b22", height=62)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="⚡ IP Management Tool",
                 bg="#161b22", fg="#58a6ff",
                 font=("Consolas", 16, "bold")).pack(side="left", padx=20, pady=14)
        tk.Label(topbar, text="Network Address Manager",
                 bg="#161b22", fg="#484f58",
                 font=("Consolas", 10)).pack(side="left", pady=14)

        # summary badges
        self.badge_total    = self._badge(topbar, "0 total",    "#21262d", "#8b949e")
        self.badge_active   = self._badge(topbar, "0 active",   "#0d2133", "#3fb950")
        self.badge_inactive = self._badge(topbar, "0 inactive", "#1a1a1a", "#6e7681")
        self.badge_reserved = self._badge(topbar, "0 reserved", "#1a1200", "#d29922")
        for b in (self.badge_reserved, self.badge_inactive,
                  self.badge_active, self.badge_total):
            b.pack(side="right", padx=(0, 10), pady=14)

        # ── search row ────────────────────────────────────────────────────────
        srow = tk.Frame(self, bg="#0d1117")
        srow.pack(fill="x", padx=20, pady=10)

        tk.Label(srow, text="🔍", bg="#0d1117", fg="#58a6ff",
                 font=("Consolas", 13)).pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_table())
        tk.Entry(srow, textvariable=self.search_var,
                 bg="#21262d", fg="#c9d1d9", insertbackground="#58a6ff",
                 font=("Consolas", 12), relief="flat", bd=0,
                 highlightthickness=1, highlightbackground="#30363d",
                 highlightcolor="#58a6ff").pack(
                     side="left", fill="x", expand=True, ipady=7)

        # status filter
        self.filter_var = tk.StringVar(value="All")
        self.filter_var.trace_add("write", lambda *_: self._refresh_table())
        filter_cb = ttk.Combobox(srow, textvariable=self.filter_var,
                                 values=["All", "Active", "Inactive", "Reserved"],
                                 state="readonly", font=("Consolas", 11), width=12)
        filter_cb.pack(side="left", padx=(10, 0), ipady=4)

        self._btn(srow, "Clear", "#21262d", "#30363d",
                  lambda: [self.search_var.set(""),
                           self.filter_var.set("All")]).pack(side="left", padx=(8, 0))

        # ── table ─────────────────────────────────────────────────────────────
        tframe = tk.Frame(self, bg="#0d1117")
        tframe.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        cols = ("#", "IP Address", "Subnet", "Hostname", "Description", "Status", "Added On")
        self.tree = ttk.Treeview(tframe, columns=cols, show="headings",
                                  style="T.Treeview", selectmode="browse")
        widths = {"#": 46, "IP Address": 140, "Subnet": 88,
                  "Hostname": 150, "Description": 230, "Status": 90, "Added On": 110}
        for col in cols:
            self.tree.heading(col, text=col,
                              command=lambda c=col: self._on_header_click(c))
            self.tree.column(col, width=widths.get(col, 120),
                             anchor="center" if col in ("#", "Subnet", "Status", "Added On") else "w",
                             stretch=col == "Description")

        vsb = ttk.Scrollbar(tframe, orient="vertical", command=self.tree.yview,
                            style="T.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("active",   background="#0d2133", foreground="#3fb950")
        self.tree.tag_configure("inactive", background="#1a1a1a", foreground="#6e7681")
        self.tree.tag_configure("reserved", background="#1a1200", foreground="#d29922")
        self.tree.tag_configure("even",     background="#0d1117", foreground="#c9d1d9")
        self.tree.tag_configure("odd",      background="#161b22", foreground="#c9d1d9")

        self.tree.bind("<Double-1>", lambda _: self._open_edit())
        self.tree.bind("<Delete>",   lambda _: self._delete())

        # ── action buttons ────────────────────────────────────────────────────
        bbar = tk.Frame(self, bg="#0d1117")
        bbar.pack(fill="x", padx=20, pady=(0, 14))

        for label, bg, hov, cmd in [
            ("＋  Add",     "#1f6feb", "#388bfd", self._open_add),
            ("✎  Edit",    "#238636", "#2ea043", self._open_edit),
            ("✕  Delete",  "#7d1a1a", "#b91c1c", self._delete),
            ("⟳  Refresh", "#21262d", "#30363d", self._refresh_table),
        ]:
            b = self._btn(bbar, label, bg, hov, cmd, bold=True, pady=8, padx=18)
            b.pack(side="left", padx=(0, 10))

        # status bar
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self, textvariable=self.status_var,
                 bg="#161b22", fg="#484f58",
                 font=("Consolas", 9), anchor="w", padx=12, pady=4
                 ).pack(fill="x", side="bottom")

    # ── helpers ───────────────────────────────────────────────────────────────

    def _badge(self, parent, text, bg, fg):
        v = tk.StringVar(value=text)
        lbl = tk.Label(parent, textvariable=v, bg=bg, fg=fg,
                       font=("Consolas", 10, "bold"), padx=10, pady=3)
        lbl._var = v
        return lbl

    def _btn(self, parent, text, bg, hover, cmd,
             bold=False, padx=10, pady=5):
        weight = "bold" if bold else "normal"
        b = tk.Button(parent, text=text, bg=bg, fg="#ffffff",
                      font=("Consolas", 11, weight),
                      relief="flat", cursor="hand2", bd=0,
                      activebackground=hover, activeforeground="#ffffff",
                      command=cmd, padx=padx, pady=pady)
        b.bind("<Enter>", lambda _, w=b, h=hover: w.config(bg=h))
        b.bind("<Leave>", lambda _, w=b, c=bg:   w.config(bg=c))
        return b

    # ── table ─────────────────────────────────────────────────────────────────

    def _refresh_table(self, *_):
        query  = self.search_var.get()
        status = self.filter_var.get() if hasattr(self, "filter_var") else "All"

        results = search_records(self.records, query)
        if status != "All":
            results = [r for r in results if r.get("status") == status]

        # sort
        col_map = {
            "IP Address": "ip", "Subnet": "subnet",
            "Hostname": "hostname", "Status": "status", "Added On": "added_on",
        }
        sk = col_map.get(self._sort_col, "ip")
        results = self._sort_results(results, key=sk, reverse=self._sort_rev)

        self.tree.delete(*self.tree.get_children())
        for row_n, rec in enumerate(results):
            status_val = rec.get("status", "Active")
            tag = {"Active": "active", "Inactive": "inactive",
                   "Reserved": "reserved"}.get(status_val,
                   "even" if row_n % 2 == 0 else "odd")
            self.tree.insert("", "end", iid=str(rec["_index"]), tags=(tag,),
                values=(
                    row_n + 1,
                    rec.get("ip", ""),
                    rec.get("subnet", ""),
                    rec.get("hostname", ""),
                    rec.get("description", ""),
                    status_val,
                    rec.get("added_on", ""),
                ))

        summary = get_summary(self.records)
        shown   = len(results)
        self.badge_total._var.set(f"{summary['total']} total")
        self.badge_active._var.set(f"{summary['active']} active")
        self.badge_inactive._var.set(f"{summary['inactive']} inactive")
        self.badge_reserved._var.set(f"{summary['reserved']} reserved")
        self.status_var.set(
            f"Showing {shown} of {summary['total']} records"
            + (f"  ·  search: '{query}'" if query.strip() else "")
            + (f"  ·  filter: {status}"  if status != "All" else "")
        )
    
    def _sort_results(self, records, key="ip", reverse=False):
        """Sort records by field. IP addresses sorted numerically."""
        if key == "ip":
            from modules.validator import ip_to_int
            def sort_key(r):
                try:
                    return ip_to_int(r.get("ip", "0.0.0.0"))
                except Exception:
                    return 0
        else:
            def sort_key(r):
                return str(r.get(key, "")).lower()
        
        return sorted(records, key=sort_key, reverse=reverse)

    def _on_header_click(self, col):
        if self._sort_col == col:
            self._sort_rev = not self._sort_rev
        else:
            self._sort_col = col
            self._sort_rev = False
        self._refresh_table()

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def _open_add(self):
        self._show_dialog(mode="add")

    def _open_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection",
                                   "Please select a record to edit.", parent=self)
            return
        self._show_dialog(mode="edit", index=int(sel[0]))

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection",
                                   "Please select a record to delete.", parent=self)
            return
        idx = int(sel[0])
        rec = self.records[idx]
        if messagebox.askyesno(
            "Confirm delete",
            f"Delete  {rec['ip']} / {rec['subnet']}?\n\nThis cannot be undone.",
            parent=self,
        ):
            self.records, deleted = delete_record(self.records, idx)
            self._refresh_table()
            self.status_var.set(f"Deleted: {deleted['ip']}")

    # ── dialog ────────────────────────────────────────────────────────────────

    def _show_dialog(self, mode="add", index=None):
        dlg = tk.Toplevel(self)
        dlg.title("Add IP Record" if mode == "add" else "Edit IP Record")
        dlg.geometry("480x440")
        dlg.configure(bg="#161b22")
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.transient(self)

        rec = self.records[index] if mode == "edit" else {}

        tk.Label(dlg,
                 text="Add new record" if mode == "add" else "Edit record",
                 bg="#161b22", fg="#58a6ff",
                 font=("Consolas", 14, "bold")).pack(pady=(22, 4), padx=26, anchor="w")
        tk.Frame(dlg, bg="#21262d", height=1).pack(fill="x", padx=26, pady=(0, 18))

        ff = tk.Frame(dlg, bg="#161b22")
        ff.pack(fill="x", padx=26)
        ff.columnconfigure(1, weight=1)

        def field(label, default, row):
            tk.Label(ff, text=label, bg="#161b22", fg="#8b949e",
                     font=("Consolas", 10)).grid(
                         row=row, column=0, sticky="w", pady=(0, 2))
            var = tk.StringVar(value=default)
            e = tk.Entry(ff, textvariable=var,
                         bg="#21262d", fg="#c9d1d9",
                         insertbackground="#58a6ff",
                         font=("Consolas", 11), relief="flat", bd=0,
                         highlightthickness=1,
                         highlightbackground="#30363d",
                         highlightcolor="#58a6ff")
            e.grid(row=row, column=1, sticky="ew", pady=(0, 12), padx=(12, 0), ipady=7)
            return var

        ip_var   = field("IP Address *", rec.get("ip", ""),          0)
        sub_var  = field("Subnet *",     rec.get("subnet", "24"),     1)
        host_var = field("Hostname",     rec.get("hostname", ""),     2)
        desc_var = field("Description",  rec.get("description", ""),  3)

        tk.Label(ff, text="Status", bg="#161b22", fg="#8b949e",
                 font=("Consolas", 10)).grid(row=4, column=0, sticky="w", pady=(0, 2))
        status_var = tk.StringVar(value=rec.get("status", "Active"))
        ttk.Combobox(ff, textvariable=status_var,
                     values=list(VALID_STATUSES),
                     state="readonly", font=("Consolas", 11)).grid(
                         row=4, column=1, sticky="ew", pady=(0, 12), padx=(12, 0), ipady=5)

        err_var = tk.StringVar()
        tk.Label(dlg, textvariable=err_var,
                 bg="#161b22", fg="#f85149",
                 font=("Consolas", 10)).pack(pady=(4, 0), padx=26, anchor="w")

        def save():
            if mode == "add":
                updated, err = add_record(
                    self.records,
                    ip_var.get(), sub_var.get(),
                    host_var.get(), desc_var.get(), status_var.get(),
                )
            else:
                updated, err = update_record(
                    self.records, index,
                    ip_var.get(), sub_var.get(),
                    host_var.get(), desc_var.get(), status_var.get(),
                )
            if err:
                err_var.set(f"⚠  {err}")
                return
            self.records = updated
            self._refresh_table()
            self.status_var.set(
                f"{'Added' if mode == 'add' else 'Updated'}: {ip_var.get().strip()}"
            )
            dlg.destroy()

        bf = tk.Frame(dlg, bg="#161b22")
        bf.pack(fill="x", padx=26, pady=(12, 22))

        label = "Save" if mode == "add" else "Update"
        self._btn(bf, label, "#1f6feb", "#388bfd", save,
                  bold=True, padx=22, pady=9).pack(side="left")
        self._btn(bf, "Cancel", "#21262d", "#30363d", dlg.destroy,
                  padx=22, pady=9).pack(side="left", padx=(10, 0))

        dlg.bind("<Return>", lambda _: save())
        dlg.bind("<Escape>", lambda _: dlg.destroy())


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = IPManagementApp()
    app.mainloop()
