"""
PRACTICAL EXAMPLE: Enterprise UI + IP Management Tool Integration
==================================================================

This example demonstrates how to integrate the enterprise UI components
with your existing IP Management Tool logic.

This shows the EASIEST way to upgrade your Main.py without major refactoring.
"""

import customtkinter as ctk
from enterprise_ui_components import (
    EnterpriseTheme,
    ModernButton,
    ModernEntry,
    ModernCard,
    ModernTable,
    ModernSidebar,
    ModernHeader,
    StatusIndicator,
)
from typing import List, Optional, Callable
import json


# ============================================================================
# INTEGRATION LAYER - Connect Business Logic to UI
# ============================================================================

class IntegratedIPManagementUI:
    """
    Example of how to integrate enterprise UI with your IP Manager logic.
    
    This shows:
    1. Loading existing data from ip_manager.py
    2. Displaying it with enterprise components
    3. Handling user interactions
    4. Updating data with modern components
    """
    
    def __init__(self):
        # Setup theme
        self.theme = EnterpriseTheme()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create root window
        self.root = ctk.CTk()
        self.root.title("IP Management Tool - Enterprise Edition")
        self.root.geometry("1600x900")
        self.root.configure(fg_color=self.theme.bg_primary)
        
        # Business logic (from your modules)
        # TODO: Initialize your IP Manager
        # from modules.ip_manager import IPManager
        # self.ip_manager = IPManager()
        # For now, we'll use sample data
        self.ip_records = self._load_sample_data()
        
        # Build UI
        self._create_ui()
    
    def _load_sample_data(self) -> List[dict]:
        """Load sample IP records (replace with actual data loading)"""
        return [
            {
                "ip": "192.168.1.1",
                "hostname": "router-main",
                "status": "active",
                "subnet": "192.168.1.0/24",
                "description": "Primary gateway"
            },
            {
                "ip": "192.168.1.10",
                "hostname": "web-server-01",
                "status": "active",
                "subnet": "192.168.1.0/24",
                "description": "Production web server"
            },
            {
                "ip": "192.168.1.20",
                "hostname": "db-server-01",
                "status": "inactive",
                "subnet": "192.168.1.0/24",
                "description": "Database backup"
            },
            {
                "ip": "192.168.1.30",
                "hostname": "workstation-01",
                "status": "active",
                "subnet": "192.168.1.0/24",
                "description": "Office workstation"
            },
            {
                "ip": "192.168.2.1",
                "hostname": "router-backup",
                "status": "active",
                "subnet": "192.168.2.0/24",
                "description": "Backup gateway"
            },
        ]
    
    def _create_ui(self):
        """Build the complete UI"""
        
        # 1. HEADER BAR
        # ============================================================
        header = ModernHeader(self.root, theme=self.theme)
        header.pack(fill="x")
        
        # 2. MAIN CONTAINER (Sidebar + Content)
        # ============================================================
        main_container = ctk.CTkFrame(self.root, fg_color=self.theme.bg_primary)
        main_container.pack(fill="both", expand=True)
        
        # 2a. SIDEBAR NAVIGATION
        # ============================================================
        sidebar = ModernSidebar(
            main_container,
            items=[
                ("🏠 Dashboard", self._show_dashboard),
                ("📊 IP Records", self._show_records),
                ("🔗 Subnets", self._show_subnets),
                ("📈 Reports", self._show_reports),
                ("💾 Backups", self._show_backups),
                ("⚙️ Settings", self._show_settings),
            ],
            theme=self.theme,
            width=250
        )
        sidebar.pack(side="left", fill="y")
        
        # 2b. CONTENT AREA
        # ============================================================
        self.content_area = ctk.CTkFrame(main_container, fg_color=self.theme.bg_primary)
        self.content_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # 3. SHOW DEFAULT VIEW (IP Records)
        # ============================================================
        self._show_records()
    
    def _show_records(self):
        """Display IP records management view"""
        self._clear_content()
        
        # Title
        title = ctk.CTkLabel(
            self.content_area,
            text="IP Records Management",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.text_primary
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # CONTROL PANEL (Add, Import, Export, Delete)
        # ========================================================
        control_card = ModernCard(
            self.content_area,
            title="Actions",
            theme=self.theme,
            height=80
        )
        control_card.pack(fill="x", pady=(0, 16))
        
        btn_frame = ctk.CTkFrame(control_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=12)
        
        add_btn = ModernButton(
            btn_frame,
            text="✚ Add Record",
            command=self._on_add_record,
            theme=self.theme,
            variant="primary"
        )
        add_btn.pack(side="left", padx=8)
        
        import_btn = ModernButton(
            btn_frame,
            text="📥 Import CSV",
            command=self._on_import,
            theme=self.theme,
            variant="primary"
        )
        import_btn.pack(side="left", padx=8)
        
        export_btn = ModernButton(
            btn_frame,
            text="📤 Export",
            command=self._on_export,
            theme=self.theme,
            variant="primary"
        )
        export_btn.pack(side="left", padx=8)
        
        delete_btn = ModernButton(
            btn_frame,
            text="🗑 Delete Selected",
            command=self._on_delete,
            theme=self.theme,
            variant="primary"
        )
        delete_btn.pack(side="left", padx=8)
        
        refresh_btn = ModernButton(
            btn_frame,
            text="🔄 Refresh",
            command=self._on_refresh,
            theme=self.theme,
            variant="primary"
        )
        refresh_btn.pack(side="left", padx=8)
        
        # SEARCH & FILTER CARD
        # ========================================================
        search_card = ModernCard(
            self.content_area,
            title="Search & Filter",
            theme=self.theme,
            height=70
        )
        search_card.pack(fill="x", pady=(0, 16))
        
        search_frame = ctk.CTkFrame(search_card, fg_color="transparent")
        search_frame.pack(fill="x", padx=16, pady=12)
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="Search:",
            font=("Segoe UI", 11),
            text_color=self.theme.text_secondary
        )
        search_label.pack(side="left", padx=(0, 8))
        
        self.search_entry = ModernEntry(
            search_frame,
            placeholder="Search by IP, hostname, or description...",
            theme=self.theme,
            width=300,
            height=32
        )
        self.search_entry.pack(side="left", padx=8)
        
        # Filter dropdown
        status_label = ctk.CTkLabel(
            search_frame,
            text="Status:",
            font=("Segoe UI", 11),
            text_color=self.theme.text_secondary
        )
        status_label.pack(side="left", padx=(16, 8))
        
        status_combo = ctk.CTkComboBox(
            search_frame,
            values=["All", "Active", "Inactive"],
            fg_color=self.theme.bg_surface_medium,
            text_color=self.theme.text_primary,
            button_color=self.theme.blue_primary,
            border_color=self.theme.border_color,
            dropdown_fg_color=self.theme.bg_surface_dark,
            dropdown_text_color=self.theme.text_primary,
            state="readonly"
        )
        status_combo.set("All")
        status_combo.pack(side="left", padx=8, fill="x")
        
        search_frame.pack_propagate(False)
        
        # DATA TABLE CARD
        # ========================================================
        table_card = ModernCard(
            self.content_area,
            title="Records",
            theme=self.theme
        )
        table_card.pack(fill="both", expand=True, pady=(0, 16))
        
        # Convert records to table format
        table_data = []
        for record in self.ip_records:
            table_data.append([
                record["ip"],
                record["hostname"],
                record["status"].upper(),
                record["subnet"],
                record["description"]
            ])
        
        table = ModernTable(
            table_card,
            columns=["IP Address", "Hostname", "Status", "Subnet", "Description"],
            data=table_data,
            theme=self.theme
        )
        table.pack(fill="both", expand=True, padx=16, pady=16)
        
        # STATISTICS CARD
        # ========================================================
        stats_frame = ctk.CTkFrame(self.content_area, fg_color=self.theme.bg_primary)
        stats_frame.pack(fill="x")
        
        # Active count
        active_count = len([r for r in self.ip_records if r["status"] == "active"])
        inactive_count = len(self.ip_records) - active_count
        
        stat1 = ModernCard(stats_frame, theme=self.theme)
        stat1.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        stat1_label = ctk.CTkLabel(
            stat1,
            text=f"Active: {active_count}",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme.color_success
        )
        stat1_label.pack(padx=16, pady=12)
        
        stat2 = ModernCard(stats_frame, theme=self.theme)
        stat2.pack(side="left", fill="both", expand=True, padx=8)
        
        stat2_label = ctk.CTkLabel(
            stat2,
            text=f"Inactive: {inactive_count}",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme.color_warning
        )
        stat2_label.pack(padx=16, pady=12)
        
        stat3 = ModernCard(stats_frame, theme=self.theme)
        stat3.pack(side="left", fill="both", expand=True, padx=(8, 0))
        
        stat3_label = ctk.CTkLabel(
            stat3,
            text=f"Total: {len(self.ip_records)}",
            font=("Segoe UI", 14, "bold"),
            text_color=self.theme.blue_primary
        )
        stat3_label.pack(padx=16, pady=12)
    
    def _show_dashboard(self):
        """Show dashboard view"""
        self._clear_content()
        
        title = ctk.CTkLabel(
            self.content_area,
            text="Dashboard",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.text_primary
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # Summary cards
        card1 = ModernCard(self.content_area, title="Total Records", theme=self.theme)
        card1.pack(fill="x", pady=8)
        
        count_label = ctk.CTkLabel(
            card1,
            text=str(len(self.ip_records)),
            font=("Segoe UI", 28, "bold"),
            text_color=self.theme.blue_primary
        )
        count_label.pack(padx=16, pady=12)
        
        card2 = ModernCard(self.content_area, title="Network Status", theme=self.theme)
        card2.pack(fill="x", pady=8)
        
        status_label = ctk.CTkLabel(
            card2,
            text="✓ All systems operational",
            font=("Segoe UI", 14),
            text_color=self.theme.color_success
        )
        status_label.pack(padx=16, pady=12)
    
    def _show_subnets(self):
        """Show subnets view"""
        self._clear_content()
        
        title = ctk.CTkLabel(
            self.content_area,
            text="Subnet Management",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.text_primary
        )
        title.pack(anchor="w", pady=(0, 20))
        
        message = ctk.CTkLabel(
            self.content_area,
            text="Subnet management coming soon",
            font=("Segoe UI", 14),
            text_color=self.theme.text_secondary
        )
        message.pack(padx=16, pady=20)
    
    def _show_reports(self):
        """Show reports view"""
        self._clear_content()
        
        title = ctk.CTkLabel(
            self.content_area,
            text="Reports & Analytics",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.text_primary
        )
        title.pack(anchor="w", pady=(0, 20))
        
        message = ctk.CTkLabel(
            self.content_area,
            text="Reports coming soon",
            font=("Segoe UI", 14),
            text_color=self.theme.text_secondary
        )
        message.pack(padx=16, pady=20)
    
    def _show_backups(self):
        """Show backups view"""
        self._clear_content()
        
        title = ctk.CTkLabel(
            self.content_area,
            text="Backups & History",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.text_primary
        )
        title.pack(anchor="w", pady=(0, 20))
        
        message = ctk.CTkLabel(
            self.content_area,
            text="Backup management coming soon",
            font=("Segoe UI", 14),
            text_color=self.theme.text_secondary
        )
        message.pack(padx=16, pady=20)
    
    def _show_settings(self):
        """Show settings view"""
        self._clear_content()
        
        title = ctk.CTkLabel(
            self.content_area,
            text="Settings",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.text_primary
        )
        title.pack(anchor="w", pady=(0, 20))
        
        message = ctk.CTkLabel(
            self.content_area,
            text="Settings coming soon",
            font=("Segoe UI", 14),
            text_color=self.theme.text_secondary
        )
        message.pack(padx=16, pady=20)
    
    def _clear_content(self):
        """Clear the content area"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    # Action handlers
    # ========================================================
    
    def _on_add_record(self):
        """Handle add record action"""
        print("Add record clicked")
        # TODO: Show add dialog
    
    def _on_import(self):
        """Handle import action"""
        print("Import clicked")
        # TODO: Call your import_export module
    
    def _on_export(self):
        """Handle export action"""
        print("Export clicked")
        # TODO: Call your export function
    
    def _on_delete(self):
        """Handle delete action"""
        print("Delete clicked")
        # TODO: Delete selected records
    
    def _on_refresh(self):
        """Handle refresh action"""
        print("Refresh clicked")
        self._show_records()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    app = IntegratedIPManagementUI()
    app.run()


# ============================================================================
# INTEGRATION CHECKLIST
# ============================================================================

"""
To integrate this with your existing IP Management Tool:

1. □ Install CustomTkinter:
     pip install customtkinter

2. □ Import your data loading logic:
     Replace _load_sample_data() with actual data from ip_manager.py
     Example: self.ip_records = self.ip_manager.get_all_records()

3. □ Implement action handlers:
     _on_add_record() → call ip_manager.add_record()
     _on_delete() → call ip_manager.delete_record()
     _on_import() → call import_export.import_csv()
     _on_export() → call import_export.export_csv()
     _on_refresh() → reload data from database

4. □ Add dialog boxes:
     Create ModernCard dialogs for Add/Edit records
     Use ModernEntry for form fields
     Use ModernButton for form actions

5. □ Connect notification system:
     Show toast/status messages
     Display error messages
     Show success confirmations

6. □ Add data validation:
     Validate IP addresses
     Check for conflicts
     Show validation errors inline

7. □ Test integration:
     Launch app and verify all actions work
     Check that data persists
     Verify error handling
     Test with sample_import.csv

8. □ Deploy:
     Update requirements.txt
     Update README with new screenshots
     Commit changes to git
"""
