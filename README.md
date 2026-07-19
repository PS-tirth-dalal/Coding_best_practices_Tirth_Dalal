# Employee Management System

A clean, well-structured **Python console application** for managing employee records, built as part of a *Coding Best Practices* assignment.

---

## Features

| Feature | Description |
|---|---|
| ➕ Add Employee | Add a new employee with full validation |
| 📋 View All | Display all employees in a formatted table |
| 🔍 Search by ID | Find an employee using their unique ID |
| ✏️ Update | Edit any field of an existing employee |
| 🗑️ Delete | Remove an employee (with confirmation prompt) |
| 🔤 Sort by Name | List employees in alphabetical order |
| 🏢 Filter by Dept | Show only employees from a specific department |
| 💾 Persist to File | Employee data saved automatically to `data/employees.json` |

---

## How to Run

### Prerequisites

- **Python 3.10 or higher** (uses union type hints `X | Y`)
- No external packages required — uses only the standard library

### Run the application

```bash
cd EmployeeManagement
python main.py
```

### Run the unit tests

```bash
cd EmployeeManagement
python -m unittest discover tests -v
```

---

## Project Structure

```
EmployeeManagement/
├── main.py                              # Entry point & menu loop
├── models/
│   └── employee.py                      # Employee dataclass & serialisation
├── services/
│   ├── employee_service.py              # Business logic (CRUD, sort, filter)
│   └── file_storage_service.py          # JSON file persistence
├── validators/
│   └── employee_validator.py            # Input validation rules
├── helpers/
│   └── console_helper.py               # Colour output, tables, prompts
├── constants/
│   └── app_constants.py                # All constants (no magic strings)
├── tests/
│   ├── test_employee_service.py        # Unit tests for service layer
│   └── test_employee_validator.py      # Unit tests for validation rules
├── data/
│   └── employees.json                   # Persisted employee data
└── requirements.txt
```

---

## Employee Fields

| Field | Required | Validation |
|---|---|---|
| Employee ID | ✅ | Must not be empty; must be unique |
| Name | ✅ | Must not be empty |
| Email | ✅ | Must match standard email format |
| Department | ✅ | Must not be empty |
| Designation | ✅ | Must not be empty |
| Joining Date | ✅ | Must be in `YYYY-MM-DD` format |

---

## Best Practices Followed

1. **Meaningful names** — PEP 8 `snake_case` for functions/variables, `PascalCase` for classes
2. **Single Responsibility Principle** — each module/class has exactly one purpose
3. **DRY (Don't Repeat Yourself)** — shared UI logic in `ConsoleHelper`, no duplicated code
4. **PEP 8 compliance** — consistent formatting throughout
5. **Input validation** — all user input validated before use; errors shown clearly
6. **Docstrings & comments** — every class and method is documented; inline comments only where needed
7. **Graceful error handling** — `try/except` prevents crashes; user-friendly messages always shown
8. **No magic strings** — every string constant lives in `app_constants.py`
9. **Type hints** — used throughout for readability and IDE support
10. **Dependency injection** — `EmployeeService` accepts a storage object, making unit testing easy
11. **Duplicate ID prevention** — adding an employee with an existing ID is rejected with a clear message
12. **Data persistence** — records saved to JSON automatically after every change

---

## Screenshots

### Main Menu
```
╔══════════════════════════════════════════════════╗
║        EMPLOYEE MANAGEMENT SYSTEM                ║
╚══════════════════════════════════════════════════╝

┌─────────────────────────────────┐
│           MAIN MENU             │
├─────────────────────────────────┤
│  1. Add Employee                │
│  2. View All Employees          │
│  3. Search Employee by ID       │
│  4. Update Employee             │
│  5. Delete Employee             │
│  6. Sort Employees by Name      │
│  7. Filter by Department        │
│  8. Exit                        │
└─────────────────────────────────┘
```

### Employee Table
```
ID         Name                 Email                        Department       Designation        Joining Date
──────────────────────────────────────────────────────────────────────────────────────────────────────────
EMP001     Alice Smith          alice@example.com            Engineering      Software Engineer  15 Jan 2024
EMP002     Bob Jones            bob@example.com              HR               HR Manager         20 Mar 2023
──────────────────────────────────────────────────────────────────────────────────────────────────────────
Total: 2 employee(s)
```

---

## Author

**Tirth Dalal** — Coding Best Practices Assignment
