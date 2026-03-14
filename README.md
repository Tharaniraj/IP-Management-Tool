# IP Management Tool

A professional Python-based GUI application for managing, tracking, and organizing IP addresses across your network infrastructure. Built with Tkinter with both JSON and SQLite backends for flexible data storage.

---

## ✨ Features

### Core CRUD Operations
- ✅ Add, edit, and delete IP address records
- ✅ Multi-select support for bulk operations
- ✅ Real-time IP conflict detection
- ✅ Hostname uniqueness validation
- ✅ Auto-save to JSON or SQLite database

### Smart Search & Organization
- 🔍 Real-time search across all fields
- 📊 Status filtering (Active/Inactive/Reserved)
- 🔀 Multi-column sorting (IP addresses sorted numerically)
- 📋 Search history infrastructure

### Bulk Operations
- 📥 Import records from CSV or JSON files
- 📤 Export visible or selected records to CSV
- 🗑️ Bulk delete with confirmation
- 🔄 Recover deleted records from recovery menu

### Data Integrity & Safety
- 💾 Automatic backups on startup (keeps last 10)
- 🗂️ Deleted records recovery with timestamps
- ⚠️ IP conflict warnings during import
- 📋 Comprehensive error logging in logs/app.log

### User Experience
- 🌙/☀️ Dark and Light theme toggle
- ⚙️ Customizable settings panel
- 🎨 Clean, professional GitHub-inspired UI
- 📱 Responsive design with resizable columns

### Database Options
- 📄 JSON storage (lightweight, portable)
- 🗄️ SQLite backend (scalable, indexed)
- 🔄 Easy migration between formats
- 📊 Database size monitoring

---

## 📋 Requirements

- Python 3.8+
- `tkinter` (built-in with Python)

**No external pip packages required** — all dependencies are from the Python standard library.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Tharaniraj/IP-Management-Tool.git
cd IP-Management-Tool
```

### 2. Run the application
```bash
python Main.py
```

---

## 📂 Project Structure

```
IP-Management-Tool/
├── Main.py                      # Application entry point & GUI
├── modules/
│   ├── __init__.py              # Module exports
│   ├── ip_manager.py            # CRUD operations
│   ├── validator.py             # IP/subnet validation
│   ├── search.py                # Search & filter functionality
│   ├── backup.py                # Backup & recovery
│   ├── logger.py                # Error logging
│   ├── import_export.py          # Bulk import/export
│   ├── database.py              # SQLite backend
│   ├── themes.py                # UI themes
│   └── core.py                  # App initialization
├── data/
│   ├── ip_data.json             # JSON data store
│   ├── ip_records.db            # SQLite database (optional)
│   ├── deleted_records.json      # Recovery records
│   └── backups/                 # Automatic backups
├── logs/
│   └── app.log                  # Application log
├── sample_import.csv            # Example CSV data
├── sample_import.json           # Example JSON data
├── requirements.txt             # Dependencies (none!)
└── README.md                    # This file
```

---

## 🎮 Usage Guide

### Adding Records
1. Click **＋ Add** button
2. Fill in IP, Subnet (CIDR or dotted notation)
3. Optionally add Hostname, Description, and Status
4. Click **Save**

### Searching & Filtering
- Use search box to filter by IP, hostname, description, etc.
- Use status dropdown to filter by Active/Inactive/Reserved
- Click column headers to sort (multi-column sorting full support)

### Bulk Operations
- **Select Multiple**: Ctrl+Click or Shift+Click to select multiple records
- **Bulk Delete**: Select records → Click **✕ Delete** → Confirm
- **Bulk Export**: Select records → Click **⇩ Export** → Choose location
- **Bulk Import**: Click **⇧ Import** → Select CSV/JSON file

### Backup & Recovery
- Automatic backups created on startup
- Click **🔄 Recover** to restore deleted records
- All deleted records kept in `/data/deleted_records.json`

### Customization
1. Click **⚙ Settings** button
2. Configure preferences:
   - IP conflict warnings on import
   - Auto-backup on startup
   - Search history display
   - Application theme (Dark/Light)

### Theme Toggle
- Click **🌙 Theme** button to quickly toggle between dark and light themes
- Change persists in settings

---

## 📊 Data Format

### CSV Import/Export
```csv
ip,subnet,hostname,description,status
192.168.1.1,24,router,Main router,Active
192.168.1.10,24,server1,Web server,Inactive
```

### JSON Format
```json
[
  {
    "ip": "192.168.1.1",
    "subnet": "24",
    "hostname": "router",
    "description": "Main router",
    "status": "Active",
    "added_on": "2026-03-14"
  }
]
```

---

## 🔒 Security & Data Safety

- **Automatic Backups**: Daily timestamped backups in `data/backups/`
- **Deleted Records Recovery**: All deletions saved for recovery
- **Validation**: Comprehensive input validation for IPs and subnets
- **Logging**: All operations logged to `logs/app.log`
- **No External Dependencies**: No third-party packages = minimal attack surface

---

## 📈 Performance

- **Fast Search**: Sub-millisecond searches with built-in optimization
- **Numeric IP Sorting**: Intelligent numerical sorting (1.1.1.1 < 1.1.1.2)
- **Scalable**: Both JSON and SQLite backends scale to thousands of records
- **Low Memory**: Lightweight Python + Tkinter stack

---

## 🛠️ Development Roadmap

### ✅ Completed Phases

**Phase 1: Quick Wins**
- Column sorting for all fields
- CSV export
- Toast notifications

**Phase 2: Robustness**
- Automatic backups on startup
- Error logging system
- Deleted records recovery
- Hostname uniqueness validation

**Phase 3: Enhanced Features**
- Bulk import (CSV/JSON)
- IP conflict detection
- Settings dialog
- Search history infrastructure

**Phase 4: Polish**
- Multi-select bulk operations
- Dark/Light theme toggle
- SQLite database backend
- Enhanced UI/UX

### 🔮 Future Enhancements
- Database migration UI (JSON ↔ SQLite)
- Advanced filtering (CIDR blocks)
- Network analysis tools
- Export to Excel with formatting
- REST API backend
- Web interface

---

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Try: `python --version`

### Data not saving
- Check folder permissions for `data/` directory
- Review `logs/app.log` for error messages

### Import errors
- Ensure CSV has proper headers: `ip,subnet,hostname,description,status`
- JSON must be an array of objects
- Review error messages in import dialog

### Theme changes don't apply
- Theme preference saved in memory
- To persist: Select preferred theme in Settings

---

## 📝 File Format Validation

### IP Address
- Valid: `192.168.1.1`, `10.0.0.1`, `255.255.255.255`
- Invalid: `256.1.1.1`, `192.168.1`, `192.168.1.1.1`

### Subnet
- CIDR: `0`, `8`, `16`, `24`, `32`
- Mask: `255.255.255.0`, `255.255.0.0`, `255.0.0.0`

### Status
- `Active` (green)
- `Inactive` (gray)
- `Reserved` (orange)

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👤 Author

**Tharaniraj**
- GitHub: [@Tharaniraj](https://github.com/Tharaniraj)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review `logs/app.log` for error details
3. Open an issue on GitHub

---

**Last Updated**: March 14, 2026
**Current Version**: 1.0.0 (Feature Complete)

