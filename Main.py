import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime

from modules import (
    load_records, add_record, update_record, delete_record, get_summary,
    search_records, sort_records, VALID_STATUSES,
    create_backup, cleanup_old_backups, save_deleted_record,
    get_deleted_records, clear_deleted_records,
    logger, log_error, log_info, log_warning, get_log_file_path,
    import_csv, import_json, detect_import_conflicts, detect_subnet_overlaps,
    get_theme, get_available_themes,
)


class IPManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IP Management Tool")
        self.geometry("1080x700")
        self.minsize(900, 580)
        self.configure(bg="#0d1117")
        self.resizable(True, True)

        # Create backup on startup
        try:
            create_backup()
            cleanup_old_backups(keep_count=10)
            log_info("Backup created successfully")
        except Exception as e:
            log_error("Failed to create backup", e)

        self.records = load_records()
        self._sort_col = "ip"
        self._sort_rev = False
        
        # Search history (in-memory)
        self._search_history = []
        self._search_history_index = -1
        
        # Theme and Settings
        self._current_theme = "dark"
        self._theme = get_theme(self._current_theme)
        self._settings = {
            "warn_conflicts": True,
            "auto_backup": True,
            "show_search_history": True,
            "theme": "dark",
        }

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
                                  style="T.Treeview", selectmode="extended")
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
            ("＋  Add",       "#1f6feb", "#388bfd", self._open_add),
            ("✎  Edit",      "#238636", "#2ea043", self._open_edit),
            ("✕  Delete",    "#7d1a1a", "#b91c1c", self._delete_selected),
            ("⇧  Import",    "#8b5cf6", "#a78bfa", self._import_records),
            ("⇩  Export",    "#1f2937", "#374151", self._export_selected),
            ("🔄 Recover",   "#6366f1", "#818cf8", self._show_recovery),
            ("🌙 Theme",     "#9333ea", "#a855f7", self._toggle_theme),
            ("⚙  Settings",  "#6b7280", "#9ca3af", self._show_settings),
            ("⟳  Refresh",   "#21262d", "#30363d", self._refresh_table),
        ]:
            b = self._btn_3d(bbar, label, bg, hov, cmd, bold=True, pady=8, padx=12)
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

    def _btn_3d(self, parent, text, bg, hover, cmd,
                bold=False, padx=12, pady=8):
        """Create a modern styled button with better visual appearance"""
        weight = "bold" if bold else "normal"
        
        # Create a frame container with padding to simulate border/3D effect
        btn_frame = tk.Frame(parent, bg=bg, highlightthickness=0)
        
        # Create the actual button inside with padding
        b = tk.Button(btn_frame, text=text, bg=bg, fg="#ffffff",
                      font=("Consolas", 11, weight),
                      relief="flat", cursor="hand2", bd=0,
                      highlightthickness=0, activebackground=hover, 
                      activeforeground="#ffffff", command=cmd, 
                      padx=padx, pady=pady)
        b.pack()
        
        # Store original colors
        b.original_bg = bg
        b.hover_bg = hover
        b.parent_frame = btn_frame
        
        # Smooth hover effects with frame effect
        def on_enter(event):
            btn_frame.config(bg=hover)
            b.config(bg=hover)
        
        def on_leave(event):
            btn_frame.config(bg=bg)
            b.config(bg=bg)
        
        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", on_leave)
        btn_frame.bind("<Enter>", on_enter)
        btn_frame.bind("<Leave>", on_leave)
        
        # Return the frame so it can be packed
        return btn_frame

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
            "Hostname": "hostname", "Description": "description",
            "Status": "status", "Added On": "added_on",
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

    def _delete_selected(self):
        """Delete selected records (supports multi-select)."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection",
                                   "Please select one or more records to delete.", parent=self)
            return
        
        # Convert IIDs to indices and sort in reverse to delete from bottom up
        indices = sorted([int(iid) for iid in sel], reverse=True)
        count = len(indices)
        
        # Get IPs for confirmation message
        ips = [self.records[idx].get("ip") for idx in indices if idx < len(self.records)]
        msg = f"Delete {count} record(s)?\n"
        if count <= 3:
            msg += "\n".join(ips)
        else:
            msg += "\n".join(ips[:3]) + f"\n... and {count - 3} more"
        msg += "\n\nThis can be recovered from the Recovery menu."
        
        if messagebox.askyesno("Confirm delete", msg, parent=self):
            for idx in indices:
                if idx < len(self.records):
                    rec = self.records[idx]
                    save_deleted_record(rec)
                    self.records.pop(idx)
            
            from modules import save_records
            save_records(self.records)
            self._refresh_table()
            self._toast(f"Deleted {count} record(s)")
            log_info(f"Bulk deleted {count} records")

    def _export_selected(self):
        """Export selected records or all visible records if none selected."""
        if not self.records:
            messagebox.showwarning("No data", "No records to export.", parent=self)
            return
        
        sel = self.tree.selection()
        
        # If records are selected, export only those; otherwise export all visible
        if sel:
            indices = [int(iid) for iid in sel]
            records_to_export = [self.records[idx] for idx in indices if idx < len(self.records)]
            export_label = f"{len(records_to_export)} selected"
        else:
            # Export all visible (filtered) records
            query = self.search_var.get()
            status = self.filter_var.get() if hasattr(self, "filter_var") else "All"
            records_to_export = search_records(self.records, query)
            if status != "All":
                records_to_export = [r for r in records_to_export if r.get("status") == status]
            export_label = f"{len(records_to_export)} visible"
        
        if not records_to_export:
            messagebox.showwarning("No data", "No records to export.", parent=self)
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"ip_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            parent=self
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["ip", "subnet", "hostname", "description", "status", "added_on"]
                )
                writer.writeheader()
                for rec in records_to_export:
                    # Remove temp '_index' field if present
                    clean_rec = {k: v for k, v in rec.items() if k != "_index"}
                    writer.writerow({
                        "ip": clean_rec.get("ip", ""),
                        "subnet": clean_rec.get("subnet", ""),
                        "hostname": clean_rec.get("hostname", ""),
                        "description": clean_rec.get("description", ""),
                        "status": clean_rec.get("status", ""),
                        "added_on": clean_rec.get("added_on", ""),
                    })
            
            self._toast(f"Exported {len(records_to_export)} records")
            log_info(f"Exported {len(records_to_export)} records to CSV")
        except Exception as e:
            log_error("Export failed", e)
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}", parent=self)


    def _toast(self, message, duration=3000):
        """Show a temporary status message that auto-dismisses."""
        self.status_var.set(message)
        # Auto-dismiss after duration (in milliseconds)
        self.after(duration, lambda: self.status_var.set("Ready"))

    def _toggle_theme(self):
        """Toggle between dark and light themes."""
        new_theme = "light" if self._current_theme == "dark" else "dark"
        self._apply_theme(new_theme)
        self._settings["theme"] = new_theme
        self._toast(f"Switched to {new_theme.capitalize()} theme")
        log_info(f"Theme changed to {new_theme}")

    def _apply_theme(self, theme_name: str):
        """Apply a theme to the entire application."""
        self._current_theme = theme_name
        self._theme = get_theme(theme_name)
        
        # Update main window background
        self.configure(bg=self._theme["bg_main"])
        
        # This is a simplified approach - a full implementation would recursively
        # update all widgets. For now, we'll just toast notification and log the change.
        # A production version would use tkinter's theme system more comprehensively.

    def _show_recovery(self):
        """Show a dialog to recover deleted records."""
        deleted_records = get_deleted_records()
        
        if not deleted_records:
            messagebox.showinfo("No Deleted Records", 
                              "No deleted records available for recovery.", parent=self)
            return
        
        dlg = tk.Toplevel(self)
        dlg.title("Recover Deleted Records")
        dlg.geometry("600x400")
        dlg.configure(bg="#161b22")
        dlg.transient(self)
        dlg.grab_set()
        
        tk.Label(dlg, text="Deleted Records", bg="#161b22", fg="#58a6ff",
                font=("Consolas", 14, "bold")).pack(pady=(12, 8), padx=16, anchor="w")
        
        # Treeview for deleted records
        cols = ("IP Address", "Subnet", "Hostname", "Deleted On")
        tree = ttk.Treeview(dlg, columns=cols, show="headings", height=10)
        widths = {"IP Address": 120, "Subnet": 80, "Hostname": 120, "Deleted On": 130}
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=widths.get(col, 100))
        
        for i, rec in enumerate(deleted_records):
            tree.insert("", "end", iid=str(i), values=(
                rec.get("ip", ""),
                rec.get("subnet", ""),
                rec.get("hostname", ""),
                rec.get("deleted_on", ""),
            ))
        
        vsb = ttk.Scrollbar(dlg, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        frame = tk.Frame(dlg, bg="#161b22")
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        tree.pack(fill="both", expand=True, side="left")
        vsb.pack(fill="y", side="right")
        
        def recover_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("No selection", 
                                     "Please select a record to recover.", parent=dlg)
                return
            
            idx = int(sel[0])
            rec_to_recover = deleted_records[idx]
            
            # Check if IP already exists
            if any(r.get("ip") == rec_to_recover.get("ip") for r in self.records):
                messagebox.showwarning("Duplicate IP",
                                     f"IP {rec_to_recover['ip']} already exists in the database.",
                                     parent=dlg)
                return
            
            # Restore the record
            self.records.append({
                "ip": rec_to_recover["ip"],
                "subnet": rec_to_recover["subnet"],
                "hostname": rec_to_recover.get("hostname", ""),
                "description": rec_to_recover.get("description", ""),
                "status": rec_to_recover.get("status", "Active"),
                "added_on": rec_to_recover.get("added_on", datetime.now().strftime("%Y-%m-%d")),
            })
            from modules import save_records
            save_records(self.records)
            
            # Remove from deleted records
            deleted_records.pop(idx)
            if deleted_records:
                import json
                from modules.backup import DELETED_FILE
                with open(DELETED_FILE, "w", encoding="utf-8") as f:
                    json.dump(deleted_records, f, indent=2, ensure_ascii=False)
            else:
                clear_deleted_records()
            
            self._refresh_table()
            self._toast(f"Recovered: {rec_to_recover['ip']}")
            log_info(f"Recovered record: {rec_to_recover['ip']}")
            dlg.destroy()
        
        # Buttons
        bframe = tk.Frame(dlg, bg="#161b22")
        bframe.pack(fill="x", padx=16, pady=(0, 12))
        
        self._btn_3d(bframe, "Recover", "#1f6feb", "#388bfd", recover_selected,
                     bold=True, padx=16, pady=9).pack(side="left")
        self._btn_3d(bframe, "Clear All", "#7d1a1a", "#b91c1c", 
                     lambda: self._confirm_clear_deleted(dlg),
                     padx=16, pady=9).pack(side="left", padx=(10, 0))
        self._btn_3d(bframe, "Close", "#21262d", "#30363d", dlg.destroy,
                     padx=16, pady=9).pack(side="left", padx=(10, 0))
    
    def _confirm_clear_deleted(self, dlg):
        """Confirm clearing all deleted records."""
        if messagebox.askyesno("Clear Deleted Records",
                             "Permanently delete all recovery records?\n\nThis cannot be undone.",
                             parent=dlg):
            clear_deleted_records()
            self._toast("Deleted records cleared")
            log_info("Cleared all deleted records")
            dlg.destroy()


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
        warn_var = tk.StringVar()
        tk.Label(dlg, textvariable=err_var,
                 bg="#161b22", fg="#f85149",
                 font=("Consolas", 10)).pack(pady=(4, 0), padx=26, anchor="w")
        tk.Label(dlg, textvariable=warn_var,
                 bg="#161b22", fg="#d29922",
                 font=("Consolas", 9)).pack(pady=(2, 0), padx=26, anchor="w")

        def save():
            ip = ip_var.get().strip()
            subnet = sub_var.get().strip()
            
            if mode == "add":
                updated, err = add_record(
                    self.records,
                    ip, subnet,
                    host_var.get(), desc_var.get(), status_var.get(),
                )
            else:
                updated, err = update_record(
                    self.records, index,
                    ip, subnet,
                    host_var.get(), desc_var.get(), status_var.get(),
                )
            
            if err:
                err_var.set(f"⚠  {err}")
                return
            
            # Check for overlapping subnets
            exclude_idx = index if mode == "edit" else -1
            overlaps = detect_subnet_overlaps(ip, subnet, self.records, exclude_idx)
            if overlaps and self._settings["warn_conflicts"]:
                warn_var.set(f"⚠  Overlaps with {len(overlaps)} existing subnet(s)")
            
            self.records = updated
            self._refresh_table()
            self._toast(
                f"{'Added' if mode == 'add' else 'Updated'}: {ip}"
            )
            dlg.destroy()

        bf = tk.Frame(dlg, bg="#161b22")
        bf.pack(fill="x", padx=26, pady=(12, 22))

        label = "Save" if mode == "add" else "Update"
        self._btn_3d(bf, label, "#1f6feb", "#388bfd", save,
                     bold=True, padx=22, pady=10).pack(side="left")
        self._btn_3d(bf, "Cancel", "#21262d", "#30363d", dlg.destroy,
                     bold=False, padx=22, pady=10).pack(side="left", padx=(10, 0))

        dlg.bind("<Return>", lambda _: save())
        dlg.bind("<Escape>", lambda _: dlg.destroy())

    def _import_records(self):
        """Import records from CSV or JSON file."""
        file_path = filedialog.askopenfilename(
            title="Import IP Records",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")],
            parent=self
        )
        
        if not file_path:
            return
        
        # Determine file type
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        try:
            if ext == ".csv":
                records, errors = import_csv(file_path)
            elif ext == ".json":
                records, errors = import_json(file_path)
            else:
                messagebox.showerror("Invalid Format", 
                                    "Please select a CSV or JSON file.", parent=self)
                return
            
            if not records and errors:
                error_msg = "\n".join(errors[:5])
                if len(errors) > 5:
                    error_msg += f"\n... and {len(errors) - 5} more errors"
                messagebox.showerror("Import Errors", error_msg, parent=self)
                return
            
            # Check for conflicts
            conflicts = detect_import_conflicts(records, self.records)
            if conflicts and self._settings["warn_conflicts"]:
                msg = f"{len(conflicts)} IP conflicts found:\n"
                msg += "\n".join(conflicts[:3])
                if len(conflicts) > 3:
                    msg += f"\n... and {len(conflicts) - 3} more"
                msg += "\n\nSkip conflicting records and import the rest?"
                
                if not messagebox.askyesno("Conflicts Detected", msg, parent=self):
                    return
                
                # Filter out conflicts
                existing_ips = {r["ip"] for r in self.records}
                records = [r for r in records if r["ip"] not in existing_ips]
            
            if not records:
                messagebox.showwarning("No Valid Records", 
                                     "All records conflict or are invalid.", parent=self)
                return
            
            # Merge records
            self.records.extend(records)
            from modules import save_records
            save_records(self.records)
            
            error_msg = f"\n".join(errors[:3]) if errors else ""
            msg = f"Successfully imported {len(records)} records"
            if errors:
                msg += f"\n{len(errors)} warnings:\n{error_msg}"
                if len(errors) > 3:
                    msg += f"\n... and {len(errors) - 3} more"
            
            messagebox.showinfo("Import Complete", msg, parent=self)
            self._refresh_table()
            self._toast(f"Imported {len(records)} records")
            log_info(f"Imported {len(records)} records from {os.path.basename(file_path)}")
        
        except Exception as e:
            log_error("Import failed", e)
            messagebox.showerror("Import Error", f"Failed to import: {str(e)}", parent=self)

    def _show_settings(self):
        """Show application settings dialog."""
        dlg = tk.Toplevel(self)
        dlg.title("Settings")
        dlg.geometry("450x380")
        dlg.configure(bg="#161b22")
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.transient(self)
        
        tk.Label(dlg, text="Settings", bg="#161b22", fg="#58a6ff",
                font=("Consolas", 14, "bold")).pack(pady=(14, 8), padx=20, anchor="w")
        tk.Frame(dlg, bg="#21262d", height=1).pack(fill="x", padx=20, pady=(0, 12))
        
        # Settings frame (scrollable would be ideal, but keeping it simple)
        sframe = tk.Frame(dlg, bg="#161b22")
        sframe.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        
        # Warn on IP conflicts
        var_conflicts = tk.BooleanVar(value=self._settings["warn_conflicts"])
        tk.Checkbutton(sframe, text="Warn about IP conflicts on import",
                      variable=var_conflicts, bg="#161b22", fg="#c9d1d9",
                      selectcolor="#1f6feb", font=("Consolas", 11)).pack(anchor="w", pady=8)
        
        # Auto backup
        var_backup = tk.BooleanVar(value=self._settings["auto_backup"])
        tk.Checkbutton(sframe, text="Automatically backup on startup",
                      variable=var_backup, bg="#161b22", fg="#c9d1d9",
                      selectcolor="#1f6feb", font=("Consolas", 11)).pack(anchor="w", pady=8)
        
        # Search history
        var_history = tk.BooleanVar(value=self._settings["show_search_history"])
        tk.Checkbutton(sframe, text="Show search history",
                      variable=var_history, bg="#161b22", fg="#c9d1d9",
                      selectcolor="#1f6feb", font=("Consolas", 11)).pack(anchor="w", pady=8)
        
        # Theme selection
        theme_frame = tk.Frame(sframe, bg="#161b22")
        theme_frame.pack(fill="x", pady=12, anchor="w")
        tk.Label(theme_frame, text="Application Theme:",
                bg="#161b22", fg="#8b949e", font=("Consolas", 10)).pack(anchor="w", pady=(0, 4))
        var_theme = tk.StringVar(value=self._current_theme)
        for theme in get_available_themes():
            tk.Radiobutton(theme_frame, text=theme.capitalize(),
                          variable=var_theme, value=theme,
                          bg="#161b22", fg="#c9d1d9", selectcolor="#1f6feb",
                          font=("Consolas", 10)).pack(anchor="w", padx=20)
        
        # Log file link
        log_frame = tk.Frame(sframe, bg="#161b22")
        log_frame.pack(fill="x", pady=16, anchor="w")
        tk.Label(log_frame, text="Log file location:",
                bg="#161b22", fg="#8b949e", font=("Consolas", 10)).pack(anchor="w")
        tk.Label(log_frame, text=get_log_file_path(),
                bg="#161b22", fg="#58a6ff", font=("Consolas", 9)).pack(anchor="w", pady=(2, 0))
        
        # Buttons
        bframe = tk.Frame(dlg, bg="#161b22")
        bframe.pack(fill="x", padx=20, pady=(0, 12))
        
        def save_settings():
            self._settings["warn_conflicts"] = var_conflicts.get()
            self._settings["auto_backup"] = var_backup.get()
            self._settings["show_search_history"] = var_history.get()
            new_theme = var_theme.get()
            if new_theme != self._current_theme:
                self._apply_theme(new_theme)
            self._toast("Settings saved")
            log_info("Settings updated")
            dlg.destroy()
        
        self._btn_3d(bframe, "Save", "#1f6feb", "#388bfd", save_settings,
                     bold=True, padx=18, pady=9).pack(side="left")
        self._btn_3d(bframe, "Cancel", "#21262d", "#30363d", dlg.destroy,
                     padx=18, pady=9).pack(side="left", padx=(10, 0))


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = IPManagementApp()
    app.mainloop()
