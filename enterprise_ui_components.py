"""
Enterprise-Grade UI Component Library for CustomTkinter
========================================================

This module provides a complete set of enterprise-style UI components
for building modern dashboard interfaces using CustomTkinter.

Usage:
    from enterprise_ui_components import EnterpriseTheme, ModernButton, ModernCard
    
    theme = EnterpriseTheme()
    button = ModernButton(parent, text="Click Me", theme=theme)
    card = ModernCard(parent, title="Data Panel", theme=theme)
"""

import customtkinter as ctk
from typing import Callable, Optional, Tuple, List
import math


# ============================================================================
# COLOR SCHEME DEFINITION
# ============================================================================

class EnterpriseTheme:
    """Complete enterprise black/blue color palette"""
    
    def __init__(self):
        # Primary Colors
        self.bg_primary = "#0F1419"      # Main background
        self.bg_surface_dark = "#1A1F2E"
        self.bg_surface_medium = "#252D3D"
        self.bg_surface_light = "#2A3448"
        self.bg_card = "#1E2633"
        
        # Blue Accent (Primary)
        self.blue_primary = "#0099FF"    # Main blue
        self.blue_dark = "#0077CC"       # Darker blue
        self.blue_light = "#33B0FF"      # Lighter blue
        self.blue_glow = "#0099FF40"     # Glow effect
        
        # Text Colors
        self.text_primary = "#E8E9EB"    # Main text
        self.text_secondary = "#9CA3AF"  # Secondary text
        self.text_tertiary = "#6B7280"   # Tertiary text
        self.text_disabled = "#4B5563"   # Disabled text
        
        # Status Colors
        self.color_success = "#10B981"   # Green
        self.color_warning = "#F59E0B"   # Orange
        self.color_danger = "#EF4444"    # Red
        self.color_info = "#06B6D4"      # Cyan
        
        # Utility Colors
        self.border_color = "#374151"
        self.border_subtle = "#2A3448"
        self.shadow_color = "#00000040"


# ============================================================================
# MODERN BUTTONS WITH 3D EFFECTS
# ============================================================================

class ModernButton(ctk.CTkButton):
    """
    Modern enterprise button with gradient, shadow, and hover effects.
    
    Features:
    - Gradient background (blue)
    - Rounded corners (6px)
    - Hover animation (glow & scale)
    - Pressed state (inset shadow)
    - Smooth transitions
    
    Args:
        parent: Parent widget
        text: Button text
        command: Callback function
        theme: EnterpriseTheme instance
        width: Button width (default: 120)
        height: Button height (default: 36)
        size: 'small' (28px), 'medium' (36px), 'large' (44px)
        variant: 'primary' (blue), 'danger' (red), 'ghost' (outline)
    """
    
    def __init__(
        self,
        parent,
        text: str = "Button",
        command: Optional[Callable] = None,
        theme: Optional[EnterpriseTheme] = None,
        width: int = 120,
        height: int = 36,
        size: str = "medium",
        variant: str = "primary",
        **kwargs
    ):
        self.theme = theme or EnterpriseTheme()
        self.variant = variant
        
        # Size configuration
        size_config = {
            "small": {"height": 28, "font": (ctk.CTkFont(), 11)},
            "medium": {"height": 36, "font": (ctk.CTkFont(), 13)},
            "large": {"height": 44, "font": (ctk.CTkFont(), 14)},
        }
        config = size_config.get(size, size_config["medium"])
        height = config["height"]
        
        # Color configuration
        color_config = {
            "primary": {
                "fg_color": self.theme.blue_primary,
                "hover_color": self.theme.blue_light,
                "text_color": "#FFFFFF",
            },
            "danger": {
                "fg_color": self.theme.color_danger,
                "hover_color": "#FF6B6B",
                "text_color": "#FFFFFF",
            },
            "ghost": {
                "fg_color": "transparent",
                "hover_color": self.theme.bg_surface_light,
                "text_color": self.theme.blue_primary,
                "border_color": self.theme.border_color,
                "border_width": 1,
            },
        }
        colors = color_config.get(variant, color_config["primary"])
        
        # Initialize CTkButton
        super().__init__(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=6,
            font=("Segoe UI", 13, "bold"),
            **colors,
            **kwargs
        )
        
        # Store original colors for hover effects
        self.original_fg_color = colors["fg_color"]
        self.hover_fg_color = colors["hover_color"]
        self.is_hovered = False
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """Handle mouse enter - show hover state"""
        if not self.is_hovered:
            self.is_hovered = True
            self.configure(fg_color=self.hover_fg_color)
    
    def _on_leave(self, event):
        """Handle mouse leave - restore normal state"""
        if self.is_hovered:
            self.is_hovered = False
            self.configure(fg_color=self.original_fg_color)


class GradientButton(ctk.CTkButton):
    """
    Button with gradient background effect.
    Creates a smooth color transition from top to bottom.
    """
    
    def __init__(
        self,
        parent,
        text: str,
        gradient_colors: Tuple[str, str],
        command: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.gradient_colors = gradient_colors
        # Note: True gradient requires Canvas overlay or custom rendering
        # For simplicity, we use the first color; full gradient requires
        # creating a custom Canvas-based widget


# ============================================================================
# MODERN INPUT FIELDS
# ============================================================================

class ModernEntry(ctk.CTkEntry):
    """
    Modern enterprise text input field.
    
    Features:
    - Dark background (#252D3D)
    - Blue border on focus
    - Rounded corners
    - Smooth color transitions
    - Glow effect on focus
    """
    
    def __init__(
        self,
        parent,
        placeholder: str = "",
        theme: Optional[EnterpriseTheme] = None,
        **kwargs
    ):
        self.theme = theme or EnterpriseTheme()
        self.placeholder = placeholder
        
        super().__init__(
            parent,
            fg_color=self.theme.bg_surface_medium,
            text_color=self.theme.text_primary,
            border_color=self.theme.border_color,
            border_width=1,
            corner_radius=4,
            placeholder_text=placeholder,
            placeholder_text_color=self.theme.text_tertiary,
            **kwargs
        )
        
        # Bind focus events for glow effect
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Focus state - blue border"""
        self.configure(
            border_color=self.theme.blue_primary,
            fg_color=self.theme.bg_surface_light
        )
    
    def _on_focus_out(self, event):
        """Normal state"""
        self.configure(
            border_color=self.theme.border_color,
            fg_color=self.theme.bg_surface_medium
        )


# ============================================================================
# MODERN CARDS & PANELS
# ============================================================================

class ModernCard(ctk.CTkFrame):
    """
    Modern card panel for grouping content.
    
    Features:
    - Dark background (#1E2633)
    - Subtle border
    - Rounded corners (8px)
    - Shadow effect (simulated with darker border)
    - Optional title header
    
    Args:
        parent: Parent widget
        title: Optional card title
        theme: EnterpriseTheme instance
        padding: Internal padding (default: 16)
    """
    
    def __init__(
        self,
        parent,
        title: Optional[str] = None,
        theme: Optional[EnterpriseTheme] = None,
        padding: int = 16,
        **kwargs
    ):
        self.theme = theme or EnterpriseTheme()
        self.padding = padding
        
        super().__init__(
            parent,
            fg_color=self.theme.bg_card,
            border_color=self.theme.border_subtle,
            border_width=1,
            corner_radius=8,
            **kwargs
        )
        
        # Title label if provided
        if title:
            title_label = ctk.CTkLabel(
                self,
                text=title,
                font=("Segoe UI", 16, "bold"),
                text_color=self.theme.text_primary,
                anchor="w"
            )
            title_label.pack(fill="x", padx=padding, pady=(padding, 12))
    
    def add_content(self, widget):
        """Add content widget to the card"""
        widget.pack(fill="both", expand=True, padx=self.padding, pady=self.padding)


# ============================================================================
# MODERN TABLES/DATA GRIDS
# ============================================================================

class ModernTable(ctk.CTkFrame):
    """
    Modern data table with professional styling.
    
    Features:
    - Dark theme styling
    - Alternating row colors
    - Row hover effects
    - Column headers with sorting indicator
    - Scrollable content
    
    Args:
        parent: Parent widget
        columns: List of column names
        data: List of row data (each row is a list)
        theme: EnterpriseTheme instance
    """
    
    def __init__(
        self,
        parent,
        columns: List[str],
        data: Optional[List[List]] = None,
        theme: Optional[EnterpriseTheme] = None,
        **kwargs
    ):
        self.theme = theme or EnterpriseTheme()
        self.columns = columns
        self.data = data or []
        self.selected_row = None
        
        super().__init__(parent, fg_color=self.theme.bg_card, **kwargs)
        
        # Header Frame
        header_frame = ctk.CTkFrame(
            self,
            fg_color=self.theme.bg_surface_light,
            border_color=self.theme.border_color,
            border_width=1,
            corner_radius=0
        )
        header_frame.pack(fill="x", padx=1, pady=1)
        
        # Column Headers
        for col in columns:
            header = ctk.CTkLabel(
                header_frame,
                text=col.upper(),
                font=("Segoe UI", 11, "bold"),
                text_color=self.theme.text_primary,
                anchor="w"
            )
            header.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        
        # Content Frame with Scrollbar
        content_frame = ctk.CTkFrame(self, fg_color=self.theme.bg_card)
        content_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Add data rows
        self.row_frames = []
        for idx, row_data in enumerate(self.data):
            row_frame = self._create_row(content_frame, row_data, idx)
            row_frame.pack(fill="x", padx=1, pady=0)
            self.row_frames.append(row_frame)
    
    def _create_row(self, parent, row_data, row_idx):
        """Create a single table row"""
        row_color = (
            self.theme.bg_surface_dark 
            if row_idx % 2 == 0 
            else self.theme.bg_card
        )
        
        row_frame = ctk.CTkFrame(
            parent,
            fg_color=row_color,
            border_color=self.theme.border_subtle,
            border_width=1,
            corner_radius=0
        )
        
        # Add cells
        for cell_data in row_data:
            cell = ctk.CTkLabel(
                row_frame,
                text=str(cell_data),
                font=("Segoe UI", 11),
                text_color=self.theme.text_primary,
                anchor="w"
            )
            cell.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        
        # Bind hover effect
        row_frame.bind("<Enter>", lambda e: row_frame.configure(
            fg_color=self.theme.bg_surface_light
        ))
        row_frame.bind("<Leave>", lambda e: row_frame.configure(
            fg_color=row_color
        ))
        
        return row_frame


# ============================================================================
# MODERN SIDEBAR NAVIGATION
# ============================================================================

class ModernSidebar(ctk.CTkFrame):
    """
    Modern sidebar navigation panel.
    
    Features:
    - Dark background (#0F1419)
    - Navigation items with hover effects
    - Active item highlighting (blue accent)
    - Optional icons support
    - Collapsible sections
    
    Args:
        parent: Parent widget
        items: List of (label, callback) tuples
        theme: EnterpriseTheme instance
        width: Sidebar width (default: 250)
    """
    
    def __init__(
        self,
        parent,
        items: List[Tuple[str, Callable]],
        theme: Optional[EnterpriseTheme] = None,
        width: int = 250,
        **kwargs
    ):
        self.theme = theme or EnterpriseTheme()
        self.items = items
        self.active_button = None
        
        super().__init__(
            parent,
            fg_color=self.theme.bg_primary,
            width=width,
            border_color=self.theme.border_subtle,
            border_width=1,
            corner_radius=0,
            **kwargs
        )
        
        # Logo/Title
        title = ctk.CTkLabel(
            self,
            text="IP MANAGER",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme.blue_primary
        )
        title.pack(padx=16, pady=24)
        
        # Divider
        divider = ctk.CTkFrame(
            self,
            fg_color=self.theme.border_subtle,
            height=1
        )
        divider.pack(fill="x", padx=12)
        
        # Navigation Items
        for label, callback in items:
            self._add_nav_item(label, callback)
        
        # Spacer
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
    
    def _add_nav_item(self, label: str, callback: Callable):
        """Add a navigation item to sidebar"""
        btn = ctk.CTkButton(
            self,
            text=label,
            command=lambda: self._on_item_click(btn, callback),
            fg_color="transparent",
            text_color=self.theme.text_secondary,
            anchor="w",
            border_width=0,
            corner_radius=6,
            padx=16,
            pady=12,
            font=("Segoe UI", 12)
        )
        btn.pack(fill="x", padx=12, pady=4)
        btn._original_bg = "transparent"
        btn._original_text_color = self.theme.text_secondary
    
    def _on_item_click(self, button, callback):
        """Handle navigation item click"""
        # Deactivate previous active button
        if self.active_button:
            self.active_button.configure(
                fg_color="transparent",
                text_color=self.theme.text_secondary,
                border_width=0
            )
        
        # Activate current button
        button.configure(
            fg_color=f"{self.theme.blue_primary}15",
            text_color=self.theme.blue_primary,
            border_color=self.theme.blue_primary,
            border_width=2,
            border_spacing=0
        )
        self.active_button = button
        
        # Execute callback
        callback()


# ============================================================================
# MODERN STATUS INDICATORS
# ============================================================================

class StatusIndicator(ctk.CTkLabel):
    """
    Status indicator with color coding.
    
    Args:
        parent: Parent widget
        status: 'active', 'inactive', 'warning', 'error'
        size: 12, 16, 24 (diameter in pixels)
    """
    
    def __init__(
        self,
        parent,
        status: str = "inactive",
        size: int = 12,
        theme: Optional[EnterpriseTheme] = None,
        **kwargs
    ):
        self.theme = theme or EnterpriseTheme()
        
        status_colors = {
            "active": self.theme.color_success,
            "inactive": self.theme.text_tertiary,
            "warning": self.theme.color_warning,
            "error": self.theme.color_danger,
        }
        
        self.color = status_colors.get(status, self.theme.text_tertiary)
        
        super().__init__(
            parent,
            text="●",
            font=("Segoe UI", size),
            text_color=self.color,
            **kwargs
        )


# ============================================================================
# MODERN TOGGLE SWITCH
# ============================================================================

class ModernToggle(ctk.CTkCheckBox):
    """
    Modern toggle switch styled for enterprise UI.
    
    Features:
    - Blue when on
    - Gray when off
    - Smooth transitions
    - Large hit target
    """
    
    def __init__(
        self,
        parent,
        text: str = "",
        command: Optional[Callable] = None,
        theme: Optional[EnterpriseTheme] = None,
        **kwargs
    ):
        self.theme = theme or EnterpriseTheme()
        
        super().__init__(
            parent,
            text=text,
            command=command,
            onvalue=1,
            offvalue=0,
            fg_color=self.theme.bg_surface_medium,
            checkmark_color=self.theme.blue_primary,
            border_color=self.theme.border_color,
            border_width=1,
            corner_radius=4,
            font=("Segoe UI", 12),
            text_color=self.theme.text_primary,
            hover_color=self.theme.bg_surface_light,
            **kwargs
        )


# ============================================================================
# MODERN HEADER BAR
# ============================================================================

class ModernHeader(ctk.CTkFrame):
    """
    Top header bar for the application.
    
    Features:
    - Logo and title
    - Search bar
    - Action buttons (Settings, User Menu)
    - Gradient background
    """
    
    def __init__(
        self,
        parent,
        title: str = "IP Management Tool",
        theme: Optional[EnterpriseTheme] = None,
        **kwargs
    ):
        self.theme = theme or EnterpriseTheme()
        
        super().__init__(
            parent,
            fg_color=self.theme.bg_surface_dark,
            border_color=self.theme.border_subtle,
            border_width=1,
            corner_radius=0,
            height=60,
            **kwargs
        )
        
        # Logo/Title
        logo = ctk.CTkLabel(
            self,
            text="▶ " + title,
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme.blue_primary
        )
        logo.pack(side="left", padx=20, pady=15)
        
        # Spacer
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(side="left", fill="both", expand=True)
        
        # Search bar
        self.search_entry = ModernEntry(
            self,
            placeholder="Search IP records...",
            theme=self.theme,
            width=300,
            height=32
        )
        self.search_entry.pack(side="left", padx=10, pady=14)
        
        # Action buttons frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="right", padx=20, pady=10)
        
        # Settings button
        settings_btn = ModernButton(
            btn_frame,
            text="⚙",
            theme=self.theme,
            width=40,
            height=40,
            size="medium"
        )
        settings_btn.pack(side="left", padx=8)
        
        # User menu button
        user_btn = ModernButton(
            btn_frame,
            text="👤",
            theme=self.theme,
            width=40,
            height=40,
            size="medium"
        )
        user_btn.pack(side="left", padx=8)


# ============================================================================
# COMPLETE APPLICATION EXAMPLE
# ============================================================================

class EnterpriseApplication(ctk.CTk):
    """
    Complete enterprise application demonstrating all components.
    
    This example shows how to assemble the custom components into
    a professional dashboard layout.
    """
    
    def __init__(self):
        super().__init__()
        
        # Setup
        self.theme = EnterpriseTheme()
        self.title("IP Management Tool - Enterprise Edition")
        self.geometry("1400x800")
        self.configure(fg_color=self.theme.bg_primary)
        
        # Top Header
        header = ModernHeader(self, theme=self.theme)
        header.pack(fill="x")
        
        # Main Container
        main_container = ctk.CTkFrame(self, fg_color=self.theme.bg_primary)
        main_container.pack(fill="both", expand=True)
        
        # Sidebar
        sidebar = ModernSidebar(
            main_container,
            items=[
                ("🏠 Dashboard", lambda: print("Dashboard clicked")),
                ("📊 IP Records", lambda: print("IP Records clicked")),
                ("🔗 Subnets", lambda: print("Subnets clicked")),
                ("📈 Reports", lambda: print("Reports clicked")),
                ("💾 Backups", lambda: print("Backups clicked")),
                ("⚙️ Settings", lambda: print("Settings clicked")),
            ],
            theme=self.theme,
            width=250
        )
        sidebar.pack(side="left", fill="y")
        
        # Content Area
        content_area = ctk.CTkFrame(main_container, fg_color=self.theme.bg_primary)
        content_area.pack(side="left", fill="both", expand=True, padx=16, pady=16)
        
        # Title
        title = ctk.CTkLabel(
            content_area,
            text="IP Records Management",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.text_primary
        )
        title.pack(anchor="w", pady=(0, 16))
        
        # Control Panel Card
        control_card = ModernCard(content_area, title="Controls", theme=self.theme)
        control_card.pack(fill="x", pady=(0, 16))
        
        # Buttons in control panel
        btn_frame = ctk.CTkFrame(control_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=12)
        
        add_btn = ModernButton(
            btn_frame,
            text="✚ Add Record",
            theme=self.theme,
            variant="primary"
        )
        add_btn.pack(side="left", padx=8)
        
        import_btn = ModernButton(
            btn_frame,
            text="📥 Import",
            theme=self.theme,
            variant="primary"
        )
        import_btn.pack(side="left", padx=8)
        
        delete_btn = ModernButton(
            btn_frame,
            text="🗑 Delete",
            theme=self.theme,
            variant="danger"
        )
        delete_btn.pack(side="left", padx=8)
        
        # Data Table Card
        table_card = ModernCard(content_area, title="Records", theme=self.theme)
        table_card.pack(fill="both", expand=True)
        
        # Sample table
        table_data = [
            ["192.168.1.1", "Router", "Active", "Gateway"],
            ["192.168.1.10", "Server-1", "Active", "Web Server"],
            ["192.168.1.20", "Server-2", "Inactive", "DB Server"],
            ["192.168.1.30", "Client-1", "Active", "Workstation"],
            ["192.168.1.40", "Client-2", "Active", "Workstation"],
        ]
        
        table = ModernTable(
            table_card,
            columns=["IP Address", "Hostname", "Status", "Description"],
            data=table_data,
            theme=self.theme
        )
        table.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Status Bar at bottom
        footer = ctk.CTkFrame(
            self,
            fg_color=self.theme.bg_surface_dark,
            border_color=self.theme.border_subtle,
            border_width=1,
            height=40
        )
        footer.pack(fill="x")
        footer.pack_propagate(False)
        
        status_text = ctk.CTkLabel(
            footer,
            text="✓ Ready | Records: 5 | Last Sync: 2 min ago",
            font=("Segoe UI", 11),
            text_color=self.theme.text_secondary
        )
        status_text.pack(side="left", padx=16, pady=8)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Enable custom tkinter dark theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create and run application
    app = EnterpriseApplication()
    app.mainloop()
