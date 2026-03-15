# Installation & Dependencies Guide

## Current Status (Before Upgrade)

Your project currently uses **zero external dependencies** - everything is from Python standard library. This is excellent! 

**Current requirements.txt:**
```
# All packages below are part of the Python standard library.
# No external pip installs are required to run this application.
```

---

## Phase 1: CustomTkinter Installation (RECOMMENDED)

For the enterprise UI upgrade, add CustomTkinter as a lightweight dependency.

### Updated requirements.txt

```txt
# IP Management Tool — Python dependencies

# Standard Library (built-in, no installation needed)
# tkinter — GUI framework (bundled with Python 3.x)
# json — data persistence
# os — file/path utilities
# re — regex for IP validation
# datetime — record timestamps

# External Dependencies (for enterprise UI)
customtkinter>=5.2.0   # Modern dark-themed GUI framework
Pillow>=9.0.0          # Image handling (optional, for icons)
```

### Installation Command

```bash
# Install CustomTkinter for enterprise UI
pip install customtkinter>=5.2.0

# Optional: Pillow for image/icon support
pip install Pillow>=9.0.0

# Or install both from requirements.txt
pip install -r requirements.txt
```

### Total Package Size
- CustomTkinter: ~2-3 MB
- Pillow (optional): ~10 MB
- Total: ~3-13 MB additional

### Python Requirements
- Python 3.8 or higher (your current Python should work)
- CustomTkinter supports: Windows, macOS, Linux

---

## Phase 2: PyQt6 Installation (Advanced Version)

For the advanced enterprise-grade version (Phase 3), you would add:

```txt
# For Phase 3 (professional enterprise version)
PyQt6>=6.5.0           # Professional GUI framework
PyQt6-sip>=13.5.0      # Required for PyQt6
```

### Installation
```bash
pip install PyQt6>=6.5.0
```

### Size: ~25 MB

---

## Installation Steps

### Step 1: Install CustomTkinter
```bash
pip install customtkinter
```

### Step 2: Verify Installation
```bash
python -c "import customtkinter; print(f'CustomTkinter {customtkinter.__version__} installed successfully')"
```

### Expected Output
```
CustomTkinter X.X.X installed successfully
```

### Step 3: Test with Example
```bash
python PRACTICAL_EXAMPLE.py
```

You should see the enterprise application launch with dark theme!

---

## Updated requirements.txt File

Replace your current requirements.txt with this:

```txt
# IP Management Tool — Python dependencies
# Version: 2.0 (Enterprise UI Edition)

# ==============================================================================
# STANDARD LIBRARY (Built-in - No Installation Needed)
# ==============================================================================
# These are included with Python 3.8+
# tkinter — GUI framework (will be replaced by customtkinter)
# json — data persistence (JSON file handling)
# os — file/path utilities (directory/file operations)
# re — regex for IP validation (input validation)
# datetime — record timestamps (date/time utilities)
# logging — error logging (debug information)
# pathlib — modern path handling (file operations)
# abc — abstract base classes (type definitions)
# typing — type hints (code documentation)
# enum — enumeration support (configuration options)

# ==============================================================================
# EXTERNAL DEPENDENCIES (For Enterprise UI)
# ==============================================================================

# GUI Framework - Modern dark-themed Tkinter replacement
customtkinter>=5.2.0

# Image handling (optional, for icons and graphics)
Pillow>=9.0.0

# ==============================================================================
# OPTIONAL DEPENDENCIES (For Phase 3 - Enterprise Professional Version)
# ==============================================================================

# Uncomment these if migrating to PyQt6 in Phase 3:
# PyQt6>=6.5.0           # Professional GUI framework
# PyQt6-sip>=13.5.0      # Required for PyQt6 (dependency)

# ==============================================================================
# DEVELOPMENT DEPENDENCIES (Optional - for testing/development)
# ==============================================================================

# pytest>=7.0.0          # Unit testing framework
# black>=22.0.0          # Code formatter
# pylint>=2.13.0         # Code linter
# mypy>=0.950            # Static type checker

# ==============================================================================
# NOTES
# ==============================================================================
# 
# Installation:
#   pip install -r requirements.txt
#
# Specific Version:
#   pip install -r requirements.txt --only-binary=:all:
#
# Upgrade All:
#   pip install --upgrade -r requirements.txt
#
# Python Version:
#   Python 3.8 or higher required
#
# Total Size:
#   Base (CustomTkinter): ~3 MB
#   With Pillow: ~13 MB
#   Phase 3 (PyQt6): +25 MB
#
```

---

## Installation Methods

### Method 1: Using requirements.txt (Recommended)
```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep customtkinter
```

### Method 2: Manual Installation
```bash
# Install CustomTkinter
pip install customtkinter

# Install Pillow (optional)
pip install Pillow

# Verify
pip show customtkinter
```

### Method 3: Upgrade Existing Installation
```bash
# Upgrade CustomTkinter if already installed
pip install --upgrade customtkinter

# Upgrade specific version
pip install customtkinter==5.2.0
```

---

## Troubleshooting Installation

### Problem: "pip: command not found"
**Solution:** Use python's pip module:
```bash
python -m pip install customtkinter
```

### Problem: "No module named 'customtkinter'"
**Solution:** Make sure you're using the correct Python version:
```bash
python --version  # Check version (should be 3.8+)
which python      # Check Python location
pip install customtkinter
```

### Problem: ModuleNotFoundError on Windows
**Solution:** Use Python launcher:
```bash
py -m pip install customtkinter
```

### Problem: Permission Denied
**Solution:** Use user installation:
```bash
pip install --user customtkinter
```

### Problem: Virtual Environment Issues
**Solution:** Activate your virtual environment first:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Then install
pip install customtkinter
```

---

## Verification

After installation, verify everything works:

```python
# test_installation.py
import sys
print(f"Python Version: {sys.version}")

# Test CustomTkinter
import customtkinter as ctk
print(f"CustomTkinter Version: {ctk.__version__}")

# Test Pillow (optional)
try:
    from PIL import Image
    print("Pillow: ✓ Installed")
except ImportError:
    print("Pillow: Not installed (optional)")

# All good!
print("\n✅ Installation successful! Ready to run enterprise UI app.")
```

Run this script:
```bash
python test_installation.py
```

Expected output:
```
Python Version: 3.9.x ...
CustomTkinter Version: 5.2.0
Pillow: ✓ Installed

✅ Installation successful! Ready to run enterprise UI app.
```

---

## Comparison: Before vs After

### Before Enterprise UI Upgrade
```txt
# Size: ~5 KB
# Dependencies: 0 external packages
# Install time: 0 seconds
# GUI Framework: tkinter (basic)
```

### After Enterprise UI Upgrade
```txt
# Size: ~15 KB + CustomTkinter (~3 MB)
# Dependencies: 1 external package (+ optional 1)
# Install time: 10-30 seconds
# GUI Framework: customtkinter (modern)
```

### After PyQt6 Migration (Phase 3)
```txt
# Size: ~20 KB + PyQt6 (~25 MB)
# Dependencies: 2 external packages
# Install time: 30-60 seconds
# GUI Framework: PyQt6 (enterprise)
```

---

## Version Pinning Guide

### Recommended: Flexible Versions
```txt
customtkinter>=5.2.0   # Accept 5.2.0 and newer
```
**Pros:** Get security updates automatically
**Cons:** Potential breaking changes

### Conservative: Exact Version
```txt
customtkinter==5.2.1   # Use only this exact version
```
**Pros:** Guaranteed compatibility
**Cons:** Miss security fixes

### Recommended for Production
```txt
customtkinter>=5.2.0,<6.0.0  # Accept 5.x but not 6.0+
```
**Pros:** Get patches, avoid major updates
**Cons:** Manual upgrade required for major versions

---

## Compatibility Matrix

| Python | CustomTkinter | PyQt6 | Status |
|--------|---------------|-------|--------|
| 3.7 | ❌ No | ❌ No | Not supported |
| 3.8 | ✅ Yes | ✅ Yes | Minimum |
| 3.9 | ✅ Yes | ✅ Yes | **Recommended** |
| 3.10 | ✅ Yes | ✅ Yes | **Recommended** |
| 3.11 | ✅ Yes | ✅ Yes | **Recommended** |
| 3.12 | ✅ Yes | ✅ Yes | Latest |

**Recommended:** Python 3.9 - 3.12

---

## Clean Installation (Fresh Start)

If you have issues, do a clean install:

```bash
# 1. Remove old environment (if using venv)
rm -rf venv
python -m venv venv

# 2. Activate new environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install from requirements
pip install -r requirements.txt

# 5. Verify
pip list
```

---

## Getting Help

### Check Installation
```bash
# List all installed packages
pip list

# Show customtkinter details
pip show customtkinter

# Check for conflicts
pip check
```

### Common Issues & Fixes
```bash
# Reinstall customtkinter
pip uninstall customtkinter -y
pip install customtkinter

# Upgrade pip first
pip install --upgrade pip
pip install customtkinter

# Use system Python
python -m pip install customtkinter
```

---

## Next Steps

1. **Update requirements.txt** with CustomTkinter
2. **Install** using: `pip install -r requirements.txt`
3. **Test** with: `python PRACTICAL_EXAMPLE.py`
4. **Verify** using the test script above
5. **Upgrade Main.py** using MIGRATION_GUIDE.md

---

## Summary

| Aspect | Details |
|--------|---------|
| **New Package** | customtkinter >= 5.2.0 |
| **Install Time** | ~10-30 seconds |
| **Package Size** | ~3 MB |
| **Python Required** | 3.8+ (you likely have this) |
| **OS Support** | Windows, macOS, Linux |
| **Installation** | `pip install customtkinter` |
| **Verification** | `python PRACTICAL_EXAMPLE.py` |

---

**You're ready to upgrade to enterprise UI! 🚀**

Go ahead and install CustomTkinter, then follow MIGRATION_GUIDE.md to upgrade your Main.py.
