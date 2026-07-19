"""
Application-wide constants.
Centralizing all constant values here avoids magic strings scattered
throughout the codebase and makes future changes easy.
"""

# ── File paths ────────────────────────────────────────────────────────────────
DATA_FILE_PATH = "data/employees.json"

# ── Menu options ──────────────────────────────────────────────────────────────
MENU_ADD_EMPLOYEE        = "1"
MENU_VIEW_ALL_EMPLOYEES  = "2"
MENU_SEARCH_EMPLOYEE     = "3"
MENU_UPDATE_EMPLOYEE     = "4"
MENU_DELETE_EMPLOYEE     = "5"
MENU_SORT_BY_NAME        = "6"
MENU_FILTER_BY_DEPT      = "7"
MENU_EXIT                = "8"

# ── Date format ───────────────────────────────────────────────────────────────
DATE_FORMAT = "%Y-%m-%d"      # Expected input: YYYY-MM-DD
DATE_FORMAT_DISPLAY = "%d %b %Y"   # Display: 15 Jan 2024

# ── Validation messages ───────────────────────────────────────────────────────
ERROR_EMPTY_EMPLOYEE_ID   = "Employee ID must not be empty."
ERROR_EMPTY_NAME          = "Name must not be empty."
ERROR_INVALID_EMAIL       = "Email address is not valid."
ERROR_EMPTY_DEPARTMENT    = "Department must not be empty."
ERROR_EMPTY_DESIGNATION   = "Designation must not be empty."
ERROR_INVALID_DATE        = f"Joining date must be in {DATE_FORMAT} format (e.g. 2024-01-15)."

# ── General messages ──────────────────────────────────────────────────────────
MSG_EMPLOYEE_ADDED        = "Employee added successfully."
MSG_EMPLOYEE_UPDATED      = "Employee updated successfully."
MSG_EMPLOYEE_DELETED      = "Employee deleted successfully."
MSG_EMPLOYEE_NOT_FOUND    = "No employee found with the given ID."
MSG_DUPLICATE_ID          = "An employee with this ID already exists."
MSG_NO_EMPLOYEES          = "No employee records found."
MSG_INVALID_CHOICE        = "Invalid choice. Please select a valid menu option."
MSG_GOODBYE               = "Goodbye! See you next time."
