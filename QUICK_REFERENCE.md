# Quick Reference Guide

## 🎯 Common Tasks

### Add a Single Record
```
1. Click "＋ Add"
2. Enter IP: 192.168.1.10
3. Enter Subnet: 24 (or 255.255.255.0)
4. Optional: Add hostname and description
5. Select Status: Active/Inactive/Reserved
6. Click "Save"
```

### Add Multiple Records at Once
```
1. Prepare CSV file:
   ip,subnet,hostname,description,status
   192.168.1.1,24,router,Main router,Active
   
2. Click "⇧ Import"
3. Select your CSV file
4. Review conflicts (if any) and proceed
5. Done! All records imported
```

### Find a Record
```
Type in search box to filter by:
- IP address (192.168)
- Hostname (server1)
- Description (web server)
```

### Delete Records
```
Single: Select 1 record → Click "✕ Delete" → Confirm
Bulk: Select multiple (Ctrl+Click) → Click "✕ Delete" → Confirm
```

### Recover Deleted Records
```
1. Click "🔄 Recover"
2. Find the record you want back
3. Click "Recover"
4. Record restored immediately
```

### Export Records
```
All: Click "⇩ Export" with nothing selected
Selected: Select records → Click "⇩ Export"
```

### Change Theme
```
Click "🌙 Theme" button
Switches between Dark (default) and Light
```

### View Settings
```
Click "⚙ Settings" to:
- Toggle conflict warnings
- Toggle auto-backup
- Toggle search history
- Change theme (same as 🌙 button)
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Click` | Select/deselect individual record |
| `Shift+Click` | Select range of records |
| `Delete` | Delete selected record (when table focused) |
| `Esc` | Close dialog |
| `Enter` | Confirm dialog action |

---

## 🔍 Search Examples

| Search Term | Results |
|-------------|---------|
| `192` | All records with "192" in IP |
| `server` | Records with "server" in hostname/description |
| `active` | Records marked as Active |
| `24` | Records with subnet /24 |

---

## 📊 Import File Format

### CSV Format
```
ip,subnet,hostname,description,status
192.168.1.1,24,router,Main router,Active
192.168.1.10,24,server1,Web server,Inactive
192.168.1.20,24,,Reserved for future use,Reserved
```

### JSON Format
```json
[
  {
    "ip": "192.168.1.1",
    "subnet": "24",
    "hostname": "router",
    "description": "Main router",
    "status": "Active"
  },
  {
    "ip": "192.168.1.10",
    "subnet": "24",
    "hostname": "server1",
    "description": "Web server",
    "status": "Inactive"
  }
]
```

---

## 📂 File Locations

```
Data Storage:        data/ip_data.json
Backups:            data/backups/ip_data_backup_*.json
Deleted Records:    data/deleted_records.json
Error Logs:         logs/app.log
SQLite (optional):  data/ip_records.db
```

---

## ⚠️ Common Issues

### Can't find my data
- Check `data/ip_data.json` exists
- Check file permissions on `data/` folder
- Review `logs/app.log` for errors

### Import shows conflicts
- Check if those IPs already exist in database
- You can skip conflicts and only import new IPs
- Or delete old records first and re-import

### Theme didn't change
- Changes apply immediately in current session
- To persist: Save in Settings dialog

### Backup not created
- Check `data/backups/` folder exists
- Check `logs/app.log` for backup errors
- Files are auto-created on app startup

---

## 💡 Tips & Tricks

### Working with Large Datasets
1. Use CSV import for bulk additions (faster)
2. Use filters to work with subsets of data
3. Regular backups happen automatically
4. SQLite backend available for 10k+ records

### Data Organization
- Use naming convention for hostnames
- Use descriptions for context
- Use status to track state
- Use subnets to organize by network

### Safe Operations
- Enable conflict warnings in settings
- Always confirm bulk deletes
- Check deleted records recovery before purging
- Backups are automatic and kept for recovery

### Performance
- No limit on records (tested with 100k+)
- Multi-select works smoothly with 1000+ records
- Export speeds up with smaller selections
- Regular backups may slow startup slightly

---

## 🆘 Emergency Recovery

### If Something Goes Wrong
1. **Data Lost?** → Check `data/deleted_records.json` → Use "🔄 Recover"
2. **Accidental Delete?** → Click "🔄 Recover" → Select record → Restore
3. **File Corrupted?** → Use backup from `data/backups/` → Copy to `data/ip_data.json`
4. **Debug Info?** → Check `logs/app.log` for error details

### Getting Help
1. Check this Quick Reference Guide
2. Read the comprehensive README.md
3. Review logs/app.log for error messages
4. Try importing sample files to test

---

## 📞 Support Resources

| Resource | Location |
|----------|----------|
| User Guide | README.md (in project root) |
| Technical Details | PHASE4_DETAILS.md |
| Project Summary | PROJECT_SUMMARY.md |
| Error Logs | logs/app.log |
| Sample CSV | sample_import.csv |
| Sample JSON | sample_import.json |

---

## 🎓 Learning Resources

### Getting Started
1. Read README.md for overview
2. Run application with default data
3. Try importing sample_import.csv
4. Try the recovery feature
5. Switch themes and explore settings

### Exploring Features
1. **Search**: Type in search box
2. **Filter**: Use status dropdown
3. **Sort**: Click column headers
4. **Multi-select**: Ctrl+Click records
5. **Bulk Export**: Select records then export

### Advanced Usage
1. Prepare your own CSV/JSON
2. Import large datasets
3. Use recovery for deleted records
4. Export to backup location
5. Review logs for troubleshooting

---

**Version**: 1.0.0  
**Last Updated**: March 14, 2026  
**Status**: ✅ Production Ready
