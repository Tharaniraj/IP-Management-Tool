# IP Management Tool

A Python-based GUI application for managing, tracking, and organizing IP addresses across your network infrastructure. Built with Tkinter and Excel/CSV as the backend for easy data portability.

---

## Features

- Add, edit, and delete IP address records (CRUD operations)
- Subnet search and filtering
- Auto-save to Excel (.xlsx) or CSV
- IP conflict detection
- Export and import support
- Clean and intuitive GUI built with Tkinter

---

## Screenshots

> _Coming soon_

---

## Requirements

- Python 3.8+
- `tkinter` (built-in with Python)
- `openpyxl` — for Excel read/write
- `pandas` — for data handling

Install dependencies:

```bash
pip install openpyxl pandas
```

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
├── main.py               # Application entry point
├── gui/
│   └── app.py            # Main GUI window
├── utils/
│   └── ip_helper.py      # IP validation and subnet utilities
├── data/
│   └── ip_database.xlsx  # Excel backend (auto-created on first run)
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
- [openpyxl](https://openpyxl.readthedocs.io/) — Excel integration
- [pandas](https://pandas.pydata.org/) — Data management

---

## Author

**Tharaniraj**
- GitHub: [@Tharaniraj](https://github.com/Tharaniraj)

---

## License

This project is licensed under the MIT License.
