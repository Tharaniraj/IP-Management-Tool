# IP Management Tool

A Python-based GUI application for managing, tracking, and organizing IP addresses across your network infrastructure. Built with Tkinter and Excel/CSV as the backend for easy data portability.

---

## Features

- Add, edit, and delete IP address records (CRUD operations)
- Subnet and IP address search and filtering
- Real-time IP conflict detection
- Auto-save to JSON data file
- Multi-column sorting and status filtering
- Clean and intuitive GUI built with Tkinter

---

## Screenshots

> _Coming soon_

---

## Requirements

- Python 3.8+
- `tkinter` (built-in with Python)

No external pip packages required — all dependencies are from the Python standard library.

---

## Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/Tharaniraj/IP-Management-Tool.git
cd IP-Management-Tool
```

2. **Run the application**

```bash
python main.py
```

---

## Project Structure

```
IP-Management-Tool/
├── Main.py               # Application entry point and GUI
├── modules/
│   ├── __init__.py       # Module exports
│   ├── ip_manager.py     # CRUD operations and data management
│   ├── validator.py      # IP and subnet validation
│   ├── search.py         # Search and filter functionality
│   └── core.py           # Core initialization
├── data/
│   └── ip_data.json      # JSON data store (auto-created on first run)
├── requirements.txt
└── README.md
```

---

## Usage

| Action         | Description                            |
|----------------|----------------------------------------|
| Add IP         | Enter IP, subnet, description and save |
| Search         | Filter by subnet or keyword            |
| Edit           | Select a record and modify fields      |
| Delete         | Remove a selected IP record            |
| Export         | Save current data to Excel or CSV      |

---

## Built With

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework
- [JSON](https://docs.python.org/3/library/json.html) — Data persistence

---

## Author

**Tharaniraj**
- GitHub: [@Tharaniraj](https://github.com/Tharaniraj)

---

## License

This project is licensed under the MIT License.
