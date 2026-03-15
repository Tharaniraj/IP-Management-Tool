"""
Enterprise-Grade UI Implementation using PyQt6
===============================================

This module provides a professional enterprise dashboard using PyQt6,
featuring advanced styling, animations, and professional UI components.

Installation:
    pip install PyQt6 PyQt6-sip

Usage:
    from enterprise_pyqt6_ui import EnterpriseApp
    
    app = EnterpriseApp()
    app.run()
"""

import sys
from typing import Optional, Callable, List, Tuple
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QFrame, QTableWidget, QTableWidgetItem,
    QScrollArea
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QColor, QFont, QIcon, QLinearGradient, QPalette, QBrush
from PyQt6.QtCore import pyqtSignal


# ============================================================================
# ENTERPRISE THEME COLORS
# ============================================================================

class ProfessionalPalette:
    """Enterprise color palette"""
    
    # Main backgrounds
    BG_PRIMARY = QColor("#0F1419")          # Main background
    BG_SURFACE_DARK = QColor("#1A1F2E")
    BG_SURFACE_MEDIUM = QColor("#252D3D")
    BG_SURFACE_LIGHT = QColor("#2A3448")
    BG_CARD = QColor("#1E2633")
    
    # Blue accent
    BLUE_PRIMARY = QColor("#0099FF")
    BLUE_DARK = QColor("#0077CC")
    BLUE_LIGHT = QColor("#33B0FF")
    
    # Text
    TEXT_PRIMARY = QColor("#E8E9EB")
    TEXT_SECONDARY = QColor("#9CA3AF")
    TEXT_TERTIARY = QColor("#6B7280")
    TEXT_DISABLED = QColor("#4B5563")
    
    # Status
    COLOR_SUCCESS = QColor("#10B981")
    COLOR_WARNING = QColor("#F59E0B")
    COLOR_DANGER = QColor("#EF4444")
    COLOR_INFO = QColor("#06B6D4")
    
    # Utility
    BORDER_COLOR = QColor("#374151")
    BORDER_SUBTLE = QColor("#2A3448")


# ============================================================================
# STYLESHEET GENERATOR
# ============================================================================

class StyleSheetFactory:
    """Generate professional stylesheets for all components"""
    
    @staticmethod
    def get_stylesheet() -> str:
        """Get complete stylesheet for application"""
        return f"""
/* MAIN APPLICATION STYLE */
QMainWindow, QWidget {{
    background-color: #{ProfessionalPalette.BG_PRIMARY.name()[1:]};
    color: #{ProfessionalPalette.TEXT_PRIMARY.name()[1:]};
}}

/* BUTTONS - PRIMARY STYLE */
QPushButton {{
    background-color: #{ProfessionalPalette.BLUE_PRIMARY.name()[1:]};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}}

QPushButton:hover {{
    background-color: #{ProfessionalPalette.BLUE_LIGHT.name()[1:]};
    border: 1px solid #{ProfessionalPalette.BLUE_PRIMARY.name()[1:]};
    box-shadow: 0 0 20px rgba(0, 153, 255, 0.5);
}}

QPushButton:pressed {{
    background-color: #{ProfessionalPalette.BLUE_DARK.name()[1:]};
    padding: 10px 14px 6px 18px;
}}

QPushButton:disabled {{
    background-color: #{ProfessionalPalette.BG_SURFACE_MEDIUM.name()[1:]};
    color: #{ProfessionalPalette.TEXT_DISABLED.name()[1:]};
}}

/* INPUT FIELDS */
QLineEdit {{
    background-color: #{ProfessionalPalette.BG_SURFACE_MEDIUM.name()[1:]};
    color: #{ProfessionalPalette.TEXT_PRIMARY.name()[1:]};
    border: 1px solid #{ProfessionalPalette.BORDER_COLOR.name()[1:]};
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
}}

QLineEdit:focus {{
    border: 2px solid #{ProfessionalPalette.BLUE_PRIMARY.name()[1:]};
    background-color: #{ProfessionalPalette.BG_SURFACE_LIGHT.name()[1:]};
}}

QLineEdit::placeholder {{
    color: #{ProfessionalPalette.TEXT_TERTIARY.name()[1:]};
}}

/* FRAMES - CARDS/PANELS */
QFrame {{
    background-color: #{ProfessionalPalette.BG_CARD.name()[1:]};
    border: 1px solid #{ProfessionalPalette.BORDER_SUBTLE.name()[1:]};
    border-radius: 8px;
}}

/* LABELS */
QLabel {{
    color: #{ProfessionalPalette.TEXT_PRIMARY.name()[1:]};
    font-family: 'Segoe UI', sans-serif;
}}

QLabel#title {{
    font-size: 24px;
    font-weight: bold;
    color: #{ProfessionalPalette.TEXT_PRIMARY.name()[1:]};
}}

QLabel#section_title {{
    font-size: 16px;
    font-weight: bold;
    color: #{ProfessionalPalette.TEXT_PRIMARY.name()[1:]};
}}

QLabel#secondary {{
    color: #{ProfessionalPalette.TEXT_SECONDARY.name()[1:]};
    font-size: 12px;
}}

/* TABLES */
QTableWidget {{
    background-color: #{ProfessionalPalette.BG_CARD.name()[1:]};
    alternate-background-color: #{ProfessionalPalette.BG_SURFACE_DARK.name()[1:]};
    gridline-color: #{ProfessionalPalette.BORDER_SUBTLE.name()[1:]};
    border: 1px solid #{ProfessionalPalette.BORDER_COLOR.name()[1:]};
    border-radius: 4px;
}}

QTableWidget::item {{
    padding: 6px;
    border: none;
    background-color: #{ProfessionalPalette.BG_CARD.name()[1:]};
}}

QTableWidget::item:alternate {{
    background-color: #{ProfessionalPalette.BG_SURFACE_DARK.name()[1:]};
}}

QTableWidget::item:selected {{
    background-color: rgba(0, 153, 255, 0.2);
    border: none;
}}

QHeaderView::section {{
    background-color: #{ProfessionalPalette.BG_SURFACE_LIGHT.name()[1:]};
    color: #{ProfessionalPalette.TEXT_PRIMARY.name()[1:]};
    padding: 8px;
    border: none;
    border-right: 1px solid #{ProfessionalPalette.BORDER_COLOR.name()[1:]};
    font-weight: bold;
    font-size: 11px;
}}

/* SCROLLBARS */
QScrollBar:vertical {{
    background-color: #{ProfessionalPalette.BG_SURFACE_DARK.name()[1:]};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: #{ProfessionalPalette.BG_SURFACE_MEDIUM.name()[1:]};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: #{ProfessionalPalette.BLUE_PRIMARY.name()[1:]};
}}

QScrollBar:horizontal {{
    background-color: #{ProfessionalPalette.BG_SURFACE_DARK.name()[1:]};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: #{ProfessionalPalette.BG_SURFACE_MEDIUM.name()[1:]};
    border-radius: 6px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: #{ProfessionalPalette.BLUE_PRIMARY.name()[1:]};
}}

/* SEPARATOR LINES */
QFrame#separator {{
    background-color: #{ProfessionalPalette.BORDER_SUBTLE.name()[1:]};
    height: 1px;
}}
"""
    
    @staticmethod
    def get_header_stylesheet() -> str:
        """Stylesheet for header bar"""
        return f"""
QFrame#header {{
    background-color: #{ProfessionalPalette.BG_SURFACE_DARK.name()[1:]};
    border-bottom: 1px solid #{ProfessionalPalette.BORDER_SUBTLE.name()[1:]};
}}
"""
    
    @staticmethod
    def get_sidebar_stylesheet() -> str:
        """Stylesheet for sidebar"""
        return f"""
QFrame#sidebar {{
    background-color: #{ProfessionalPalette.BG_PRIMARY.name()[1:]};
    border-right: 1px solid #{ProfessionalPalette.BORDER_SUBTLE.name()[1:]};
}}

QPushButton#nav_item {{
    background-color: transparent;
    border: none;
    padding: 12px 16px;
    text-align: left;
    color: #{ProfessionalPalette.TEXT_SECONDARY.name()[1:]};
    font-size: 12px;
    border-radius: 6px;
}}

QPushButton#nav_item:hover {{
    background-color: #{ProfessionalPalette.BG_SURFACE_MEDIUM.name()[1:]};
    color: #{ProfessionalPalette.TEXT_PRIMARY.name()[1:]};
    box-shadow: none;
}}

QPushButton#nav_item_active {{
    background-color: rgba(0, 153, 255, 0.1);
    color: #{ProfessionalPalette.BLUE_PRIMARY.name()[1:]};
    border: none;
    border-left: 3px solid #{ProfessionalPalette.BLUE_PRIMARY.name()[1:]};
    padding-left: 13px;
}}
"""


# ============================================================================
# MODERN BUTTON WITH ANIMATIONS
# ============================================================================

class AnimatedButton(QPushButton):
    """Button with hover and press animations"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(36)
        self.setMinimumWidth(100)
        
        # Animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(100)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def enterEvent(self, event):
        """Hover animation"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Restore from hover"""
        super().leaveEvent(event)


# ============================================================================
# HEADER BAR COMPONENT
# ============================================================================

class HeaderBar(QFrame):
    """Modern header with search and actions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("header")
        self.setStyleSheet(StyleSheetFactory.get_header_stylesheet())
        self.setFixedHeight(60)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(12)
        
        # Logo and title
        title = QLabel("▶ IP Management Tool")
        title_font = QFont("Segoe UI", 16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: #{ProfessionalPalette.BLUE_PRIMARY.name()[1:]};")
        layout.addWidget(title)
        
        # Spacer
        layout.addStretch()
        
        # Search bar
        search = QLineEdit()
        search.setPlaceholderText("Search IP records...")
        search.setFixedWidth(300)
        search.setFixedHeight(32)
        layout.addWidget(search)
        
        # Action buttons
        settings_btn = AnimatedButton("⚙")
        settings_btn.setFixedSize(40, 40)
        layout.addWidget(settings_btn)
        
        user_btn = AnimatedButton("👤")
        user_btn.setFixedSize(40, 40)
        layout.addWidget(user_btn)


# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

class SidebarNavigation(QFrame):
    """Modern sidebar with navigation items"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setStyleSheet(StyleSheetFactory.get_sidebar_stylesheet())
        self.setFixedWidth(250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(4)
        
        # Logo
        logo = QLabel("IP MANAGER")
        logo_font = QFont("Segoe UI", 14)
        logo_font.setBold(True)
        logo.setFont(logo_font)
        logo.setStyleSheet(f"color: #{ProfessionalPalette.BLUE_PRIMARY.name()[1]}; padding: 0px 16px;")
        layout.addWidget(logo)
        
        # Divider
        divider = QFrame()
        divider.setObjectName("separator")
        divider.setFixedHeight(1)
        layout.addWidget(divider)
        
        # Navigation items
        nav_items = [
            ("🏠 Dashboard", lambda: print("Dashboard")),
            ("📊 IP Records", lambda: print("IP Records")),
            ("🔗 Subnets", lambda: print("Subnets")),
            ("📈 Reports", lambda: print("Reports")),
            ("💾 Backups", lambda: print("Backups")),
            ("⚙️ Settings", lambda: print("Settings")),
        ]
        
        self.active_btn = None
        for item_text, callback in nav_items:
            btn = QPushButton(item_text)
            btn.setObjectName("nav_item")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, cb=callback: self._on_nav_click(btn, cb))
            layout.addWidget(btn)
        
        # Spacer
        layout.addStretch()
    
    def _on_nav_click(self, button: QPushButton, callback: Callable):
        """Handle navigation click"""
        # Remove active style from previous button
        if self.active_btn:
            self.active_btn.setObjectName("nav_item")
            self.active_btn.style().unpolish(self.active_btn)
            self.active_btn.style().polish(self.active_btn)
        
        # Set active style
        button.setObjectName("nav_item_active")
        button.style().unpolish(button)
        button.style().polish(button)
        self.active_btn = button
        
        # Execute callback
        callback()


# ============================================================================
# DATA TABLE COMPONENT
# ============================================================================

class DataTable(QTableWidget):
    """Professional data table with styling"""
    
    def __init__(self, columns: List[str], rows: Optional[List[List[str]]] = None, parent=None):
        super().__init__(parent)
        
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        
        # Styling
        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Add rows if provided
        if rows:
            self.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.setItem(row_idx, col_idx, item)
        
        self.setMinimumHeight(300)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class EnterpriseApp(QMainWindow):
    """Complete enterprise application using PyQt6"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Management Tool - Enterprise Edition")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(StyleSheetFactory.get_stylesheet())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top layout (header at top)
        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        
        # Header
        header = HeaderBar()
        top_layout.addWidget(header)
        
        # Content layout (sidebar + content)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        sidebar = SidebarNavigation()
        content_layout.addWidget(sidebar)
        
        # Main content area
        content_area = QWidget()
        content_layout.addWidget(content_area, 1)
        content_area.setStyleSheet(f"background-color: #{ProfessionalPalette.BG_PRIMARY.name()[1:]};")
        
        content_area_layout = QVBoxLayout(content_area)
        content_area_layout.setContentsMargins(24, 24, 24, 24)
        content_area_layout.setSpacing(16)
        
        # Title
        title = QLabel("IP Records Management")
        title.setObjectName("title")
        content_area_layout.addWidget(title)
        
        # Control panel
        control_panel = QFrame()
        control_layout = QHBoxLayout(control_panel)
        control_layout.setContentsMargins(16, 12, 16, 12)
        control_layout.setSpacing(8)
        
        add_btn = AnimatedButton("✚ Add Record")
        import_btn = AnimatedButton("📥 Import")
        export_btn = AnimatedButton("📤 Export")
        delete_btn = AnimatedButton("🗑 Delete")
        delete_btn.setStyleSheet(delete_btn.styleSheet() + f"""
            QPushButton {{
                background-color: #{ProfessionalPalette.COLOR_DANGER.name()[1:]};
            }}
            QPushButton:hover {{
                background-color: #ff6b6b;
            }}
        """)
        
        control_layout.addWidget(add_btn)
        control_layout.addWidget(import_btn)
        control_layout.addWidget(export_btn)
        control_layout.addWidget(delete_btn)
        control_layout.addStretch()
        
        content_area_layout.addWidget(control_panel)
        
        # Data table
        table_data = [
            ["192.168.1.1", "Router", "Active", "Gateway", "Network"],
            ["192.168.1.10", "Server-01", "Active", "Web Server", "Production"],
            ["192.168.1.20", "Server-02", "Inactive", "Database", "Standby"],
            ["192.168.1.30", "Client-01", "Active", "Workstation", "Office"],
            ["192.168.1.40", "Client-02", "Active", "Workstation", "Office"],
            ["192.168.1.50", "Printer-01", "Active", "Network Printer", "Shared"],
        ]
        
        table = DataTable(
            columns=["IP Address", "Hostname", "Status", "Type", "Location"],
            rows=table_data
        )
        content_area_layout.addWidget(table, 1)
        
        # Status bar
        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background-color: #{ProfessionalPalette.BG_SURFACE_DARK.name()[1:]};
                color: #{ProfessionalPalette.TEXT_SECONDARY.name()[1:]};
                border-top: 1px solid #{ProfessionalPalette.BORDER_SUBTLE.name()[1:]};
                padding: 6px;
                font-size: 11px;
            }}
        """)
        self.statusBar().showMessage("✓ Ready | Records: 6 | Last Sync: 2 min ago")
        
        # Combine layouts
        top_layout.addLayout(content_layout, 1)
        main_layout.addLayout(top_layout)
        
        # Apply stylesheet
        self.setStyleSheet(StyleSheetFactory.get_stylesheet())
    
    def run(self):
        """Display and run the application"""
        self.show()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnterpriseApp()
    window.run()
    sys.exit(app.exec())
