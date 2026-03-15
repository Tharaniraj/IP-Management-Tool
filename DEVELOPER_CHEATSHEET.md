"""
COMPONENT CHEATSHEET - Enterprise UI Quick Reference
=====================================================

Cheat sheet for using enterprise UI components in your application.
Keep this open while developing!
"""

# ==============================================================================
# SECTION 1: SETUP & INITIALIZATION
# ==============================================================================

"""
SETUP - 3 LINES TO GET STARTED
================================

from enterprise_ui_components import EnterpriseTheme
import customtkinter as ctk

# 1. Enable dark mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 2. Create theme
theme = EnterpriseTheme()

# 3. Create window
root = ctk.CTk()
root.configure(fg_color=theme.bg_primary)

# That's it! Now use components with:  component(..., theme=theme)
"""


# ==============================================================================
# SECTION 2: COMPONENT QUICK REFERENCE
# ==============================================================================

"""
QUICK COMPONENT REFERENCE
===========================

╔════════════════════════════════════════════════════════════════╗
║ 1. MODERN BUTTON                                              ║
╚════════════════════════════════════════════════════════════════╝

from enterprise_ui_components import ModernButton

# Basic button
btn = ModernButton(
    parent,
    text="Click Me",
    command=my_function,
    theme=theme
)
btn.pack()

# Button variants
btn_primary = ModernButton(parent, text="Save", theme=theme, variant="primary")
btn_danger = ModernButton(parent, text="Delete", theme=theme, variant="danger")
btn_ghost = ModernButton(parent, text="Cancel", theme=theme, variant="ghost")

# Button sizes
btn_small = ModernButton(parent, text="Small", theme=theme, size="small")       # 28px
btn_medium = ModernButton(parent, text="Normal", theme=theme, size="medium")    # 36px (default)
btn_large = ModernButton(parent, text="Large", theme=theme, size="large")       # 44px


╔════════════════════════════════════════════════════════════════╗
║ 2. MODERN ENTRY (Text Input)                                  ║
╚════════════════════════════════════════════════════════════════╝

from enterprise_ui_components import ModernEntry

# Basic input
entry = ModernEntry(
    parent,
    placeholder="Enter text...",
    theme=theme
)
entry.pack()

# Get value
value = entry.get()

# Set value
entry.insert(0, "Default text")

# Clear
entry.delete(0, "end")

# Get focus
entry.focus()

# Disable
entry.configure(state="disabled")


╔════════════════════════════════════════════════════════════════╗
║ 3. MODERN CARD (Container/Panel)                              ║
╚════════════════════════════════════════════════════════════════╝

from enterprise_ui_components import ModernCard

# Basic card with title
card = ModernCard(
    parent,
    title="My Card Title",
    theme=theme
)
card.pack(fill="x", pady=8)

# Add content to card
button = ctk.CTkButton(card, text="Button in card")
button.pack(padx=16, pady=12)

# Card without title
card_no_title = ModernCard(parent, theme=theme)

# Nested cards
inner_card = ModernCard(card, title="Nested Card", theme=theme)
inner_card.pack(fill="both", expand=True, padx=16, pady=12)


╔════════════════════════════════════════════════════════════════╗
║ 4. MODERN TABLE (Data Grid)                                   ║
╚════════════════════════════════════════════════════════════════╝

from enterprise_ui_components import ModernTable

# Create table with data
data = [
    ["192.168.1.1", "Router", "Active"],
    ["192.168.1.10", "Server", "Inactive"],
]

table = ModernTable(
    parent,
    columns=["IP Address", "Hostname", "Status"],
    data=data,
    theme=theme
)
table.pack(fill="both", expand=True)

# Update table with new data
# To refresh: destroy and recreate the table
for widget in parent.winfo_children():
    widget.destroy()
new_table = ModernTable(parent, columns=["IP", "Host", "Status"], data=new_data, theme=theme)
new_table.pack(fill="both", expand=True)


╔════════════════════════════════════════════════════════════════╗
║ 5. MODERN SIDEBAR (Navigation)                                ║
╚════════════════════════════════════════════════════════════════╝

from enterprise_ui_components import ModernSidebar

sidebar = ModernSidebar(
    parent,
    items=[
        ("🏠 Dashboard", lambda: print("Dashboard")),
        ("📊 Records", lambda: print("Records")),
        ("⚙️ Settings", lambda: print("Settings")),
    ],
    theme=theme,
    width=250  # Optional: default is 250
)
sidebar.pack(side="left", fill="y")


╔════════════════════════════════════════════════════════════════╗
║ 6. MODERN HEADER (Top Bar)                                    ║
╚════════════════════════════════════════════════════════════════╝

from enterprise_ui_components import ModernHeader

header = ModernHeader(
    parent,
    title="My Application",
    theme=theme
)
header.pack(fill="x")

# Access search entry for binding:
# header.search_entry.get()


╔════════════════════════════════════════════════════════════════╗
║ 7. STATUS INDICATOR (Status Dot)                              ║
╚════════════════════════════════════════════════════════════════╝

from enterprise_ui_components import StatusIndicator

# Create indicator
indicator_active = StatusIndicator(parent, status="active", theme=theme)
indicator_inactive = StatusIndicator(parent, status="inactive", theme=theme)
indicator_warning = StatusIndicator(parent, status="warning", theme=theme)
indicator_error = StatusIndicator(parent, status="error", theme=theme)

indicator_active.pack()

# Sizes
small_indicator = StatusIndicator(parent, status="active", size=12, theme=theme)
large_indicator = StatusIndicator(parent, status="active", size=24, theme=theme)


╔════════════════════════════════════════════════════════════════╗
║ 8. MODERN TOGGLE (Checkbox)                                   ║
╚════════════════════════════════════════════════════════════════╝

from enterprise_ui_components import ModernToggle

toggle = ModernToggle(
    parent,
    text="Enable Backups",
    command=lambda: print("Toggled"),
    theme=theme
)
toggle.pack()

# Get value
is_enabled = toggle.get()  # 1 or 0

# Set value
toggle.select()     # Turn on
toggle.deselect()   # Turn off
"""


# ==============================================================================
# SECTION 3: LAYOUT PATTERNS
# ==============================================================================

"""
COMMON LAYOUT PATTERNS
======================

PATTERN 1: Header + Sidebar + Content
─────────────────────────────────────
root = ctk.CTk()

header = ModernHeader(root, theme=theme)
header.pack(fill="x")

main = ctk.CTkFrame(root, fg_color=theme.bg_primary)
main.pack(fill="both", expand=True)

sidebar = ModernSidebar(main, items=[...], theme=theme)
sidebar.pack(side="left", fill="y")

content = ctk.CTkFrame(main, fg_color=theme.bg_primary)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)


PATTERN 2: Form Layout (With Validation)
─────────────────────────────────────────
form_card = ModernCard(parent, title="User Form", theme=theme)
form_card.pack(fill="x", pady=8)

# Labels and inputs
label = ctk.CTkLabel(form_card, text="IP Address:", text_color=theme.text_secondary)
label.pack(anchor="w", padx=16, pady=(12, 4))

ip_entry = ModernEntry(form_card, placeholder="192.168.1.1", theme=theme)
ip_entry.pack(fill="x", padx=16, pady=(0, 12))

# Buttons
btn_frame = ctk.CTkFrame(form_card, fg_color="transparent")
btn_frame.pack(fill="x", padx=16, pady=12)

save_btn = ModernButton(btn_frame, text="Save", theme=theme, variant="primary")
save_btn.pack(side="left", padx=4)

cancel_btn = ModernButton(btn_frame, text="Cancel", theme=theme, variant="ghost")
cancel_btn.pack(side="left", padx=4)


PATTERN 3: Dashboard with Statistics
─────────────────────────────────────
# Title
title = ctk.CTkLabel(parent, text="Dashboard", font=("Segoe UI", 24, "bold"), text_color=theme.text_primary)
title.pack(anchor="w", pady=(0, 20))

# Stats row
stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
stats_frame.pack(fill="x", pady=16)

stat1 = ModernCard(stats_frame, theme=theme)
stat1.pack(side="left", fill="both", expand=True, padx=4)
stat1_label = ctk.CTkLabel(stat1, text="Total: 42", font=("Segoe UI", 16, "bold"), text_color=theme.blue_primary)
stat1_label.pack(padx=16, pady=12)

stat2 = ModernCard(stats_frame, theme=theme)
stat2.pack(side="left", fill="both", expand=True, padx=4)
stat2_label = ctk.CTkLabel(stat2, text="Active: 38", font=("Segoe UI", 16, "bold"), text_color=theme.color_success)
stat2_label.pack(padx=16, pady=12)

# Chart/Table
data_card = ModernCard(parent, title="Recent Activity", theme=theme)
data_card.pack(fill="both", expand=True, pady=16)


PATTERN 4: Search + Filter + Results
─────────────────────────────────────
# Search card
search_card = ModernCard(parent, title="Search", theme=theme)
search_card.pack(fill="x", pady=8)

search_frame = ctk.CTkFrame(search_card, fg_color="transparent")
search_frame.pack(fill="x", padx=16, pady=12)

search_entry = ModernEntry(search_frame, placeholder="Search...", theme=theme)
search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

filter_combo = ctk.CTkComboBox(search_frame, values=["All", "Active", "Inactive"], state="readonly")
filter_combo.pack(side="left", padx=4)

search_btn = ModernButton(search_frame, text="Search", theme=theme)
search_btn.pack(side="left", padx=4)

# Results table
results_card = ModernCard(parent, title="Results", theme=theme)
results_card.pack(fill="both", expand=True, pady=8)

table = ModernTable(results_card, columns=["Name", "Status"], data=[], theme=theme)
table.pack(fill="both", expand=True, padx=16, pady=16)
"""


# ==============================================================================
# SECTION 4: COLOR REFERENCE
# ==============================================================================

"""
COLOR REFERENCE
================

BACKGROUND COLORS
─────────────────
theme.bg_primary          = "#0F1419"   (Main background - darkest)
theme.bg_surface_dark     = "#1A1F2E"   (For dark components)
theme.bg_surface_medium   = "#252D3D"   (For inputs, filters)
theme.bg_surface_light    = "#2A3448"   (For headers, hover states)
theme.bg_card             = "#1E2633"   (For cards/panels)

TEXT COLORS
──────────
theme.text_primary        = "#E8E9EB"   (Main text - use this most)
theme.text_secondary      = "#9CA3AF"   (Labels, secondary text)
theme.text_tertiary       = "#6B7280"   (Hints, disabled text)
theme.text_disabled       = "#4B5563"   (Disabled elements)

ACCENT COLORS
────────────
theme.blue_primary        = "#0099FF"   (Main accent - buttons, highlights)
theme.blue_dark           = "#0077CC"   (Darker blue - hover, pressed)
theme.blue_light          = "#33B0FF"   (Lighter blue - glow, highlights)

STATUS COLORS
─────────────
theme.color_success       = "#10B981"   (Green - success, active)
theme.color_warning       = "#F59E0B"   (Orange - warning, caution)
theme.color_danger        = "#EF4444"   (Red - error, delete)
theme.color_info          = "#06B6D4"   (Cyan - info, notice)

BORDER COLORS
─────────────
theme.border_color        = "#374151"   (Standard borders)
theme.border_subtle       = "#2A3448"   (Subtle borders)

USAGE EXAMPLES:
───────────────
# Button text (always white or primary text)
button_text = "#FFFFFF" or theme.text_primary

# Card background
card_bg = theme.bg_card

# Input border normal
input_border = theme.border_color

# Input border focus
input_border_focus = theme.blue_primary

# Label text
label_text = theme.text_secondary

# Status indicator
status_active = theme.color_success
status_error = theme.color_danger
"""


# ==============================================================================
# SECTION 5: COMMON TASKS
# ==============================================================================

"""
COMMON TASKS & SOLUTIONS
==========================

TASK 1: Create a form to add a new record
──────────────────────────────────────────
from enterprise_ui_components import ModernCard, ModernButton, ModernEntry
import customtkinter as ctk

form = ModernCard(parent, title="Add New IP", theme=theme)
form.pack(fill="x", pady=8)

# IP Address field
ip_label = ctk.CTkLabel(form, text="IP Address:", text_color=theme.text_secondary)
ip_label.pack(anchor="w", padx=16, pady=(12, 4))
ip_entry = ModernEntry(form, placeholder="192.168.1.1", theme=theme)
ip_entry.pack(fill="x", padx=16, pady=(0, 8))

# Hostname field
hostname_label = ctk.CTkLabel(form, text="Hostname:", text_color=theme.text_secondary)
hostname_label.pack(anchor="w", padx=16, pady=(8, 4))
hostname_entry = ModernEntry(form, placeholder="router-01", theme=theme)
hostname_entry.pack(fill="x", padx=16, pady=(0, 8))

# Buttons
buttonframe = ctk.CTkFrame(form, fg_color="transparent")
buttonframe.pack(fill="x", padx=16, pady=12)

save_btn = ModernButton(buttonframe, text="Save", theme=theme, variant="primary")
save_btn.pack(side="left", padx=4)
cancel_btn = ModernButton(buttonframe, text="Cancel", theme=theme, variant="ghost")
cancel_btn.pack(side="left", padx=4)

# Get values when save clicked:
# ip = ip_entry.get()
# hostname = hostname_entry.get()


TASK 2: Refresh a table with new data
──────────────────────────────────────
# Store table reference
self.table_container = ctk.CTkFrame(parent, fg_color=theme.bg_card)
self.table_container.pack(fill="both", expand=True)

# To refresh:
for widget in self.table_container.winfo_children():
    widget.destroy()

new_table = ModernTable(
    self.table_container,
    columns=["IP", "Hostname", "Status"],
    data=new_data,
    theme=theme
)
new_table.pack(fill="both", expand=True, padx=16, pady=16)


TASK 3: Show success/error messages
────────────────────────────────────
# Create a simple message label
msg_label = ctk.CTkLabel(
    parent,
    text="✓ Record saved successfully!",
    text_color=theme.color_success,
    font=("Segoe UI", 12)
)
msg_label.pack(pady=8)

# Auto-hide after 3 seconds
parent.after(3000, msg_label.pack_forget)

# For errors:
error_label = ctk.CTkLabel(
    parent,
    text="✗ Error: Invalid IP address",
    text_color=theme.color_danger,
    font=("Segoe UI", 12)
)
error_label.pack(pady=8)


TASK 4: Create a multi-select action menu
──────────────────────────────────────────
frame = ctk.CTkFrame(parent, fg_color=theme.bg_card)
frame.pack(fill="x", padx=8, pady=8)

# Checkbox label
checkbox = ctk.CTkCheckBox(frame, text="Select all rows")
checkbox.pack(side="left", padx=12, pady=8)

# Action buttons
actions_frame = ctk.CTkFrame(frame, fg_color="transparent")
actions_frame.pack(side="right", padx=12, pady=8)

export_btn = ModernButton(actions_frame, text="Export Selected", theme=theme)
export_btn.pack(side="left", padx=4)

delete_btn = ModernButton(actions_frame, text="Delete Selected", theme=theme, variant="danger")
delete_btn.pack(side="left", padx=4)


TASK 5: Add a status indicator to a row
────────────────────────────────────────
from enterprise_ui_components import StatusIndicator

row_frame = ctk.CTkFrame(parent, fg_color=theme.bg_surface_dark)
row_frame.pack(fill="x", pady=4)

status_indicator = StatusIndicator(row_frame, status="active", theme=theme)
status_indicator.pack(side="left", padx=12)

ip_label = ctk.CTkLabel(row_frame, text="192.168.1.1", text_color=theme.text_primary)
ip_label.pack(side="left", padx=8)

hostname_label = ctk.CTkLabel(row_frame, text="router-01", text_color=theme.text_secondary)
hostname_label.pack(side="left", padx=8)
"""


# ==============================================================================
# SECTION 6: TROUBLESHOOTING
# ==============================================================================

"""
TROUBLESHOOTING QUICK FIXES
============================

PROBLEM: Button doesn't respond to clicks
SOLUTION: Make sure you pass command parameter:
    ❌ ModernButton(parent, text="Click", theme=theme)  # Wrong
    ✅ ModernButton(parent, text="Click", command=my_func, theme=theme)  # Correct

PROBLEM: Text appears blurry
SOLUTION: Use system fonts, specify size:
    ❌ font="Arial"  # Too vague
    ✅ font=("Segoe UI", 13)  # Specific size

PROBLEM: Colors look wrong
SOLUTION: Check theme is passed to all components:
    ❌ ModernButton(parent, text="OK")  # Uses default
    ✅ ModernButton(parent, text="OK", theme=theme)  # Uses your theme

PROBLEM: Layout is crashing
SOLUTION: Check pack() parameters:
    ❌ widget.pack()  # Might overlap
    ✅ widget.pack(fill="x")  # Proper sizing

PROBLEM: Table doesn't show data
SOLUTION: Check data format - must be List[List[str]]:
    ❌ data = {"ip": "192.168.1.1"}  # Wrong - dict
    ✅ data = [["192.168.1.1", "router"]]  # Correct - list of lists

PROBLEM: Performance is slow
SOLUTION: 
    1. Reduce theme updates (pass once, reuse)
    2. Don't recreate widgets frequently
    3. Use after() for delayed operations
    4. Limit table rows (use pagination for 1000+ rows)

PROBLEM: Sidebar won't activate items
SOLUTION: Sidebar tracks active button internally:
    ✅ Just click sidebar items - they'll highlight automatically

PROBLEM: Component is too small/large
SOLUTION: Use size parameter or set dimensions:
    ✅ ModernButton(parent, text="OK", size="large", theme=theme)
    ✅ ModernButton(parent, text="OK", width=150, height=40, theme=theme)
"""
