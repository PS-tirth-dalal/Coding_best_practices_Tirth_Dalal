"""
Employee input validator.

All validation rules live here so that business logic and UI code
stay clean and do not embed validation details.
"""

import re
from datetime import datetime
from models.employee import Employee
from constants.app_constants import (
    DATE_FORMAT,
    ERROR_EMPTY_EMPLOYEE_ID,
    ERROR_EMPTY_NAME,
    ERROR_INVALID_EMAIL,
    ERROR_EMPTY_DEPARTMENT,
    ERROR_EMPTY_DESIGNATION,
    ERROR_INVALID_DATE,
)

# Regex pattern for a basic but robust email check
_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


class EmployeeValidator:
    """Validates employee data before it is saved or updated."""

    @staticmethod
    def validate(employee: Employee) -> list[str]:
        """
        Run all validation rules against the given employee.

        Returns:
            A list of error message strings. An empty list means the data is valid.
        """
        errors: list[str] = []

        if not employee.employee_id.strip():
            errors.append(ERROR_EMPTY_EMPLOYEE_ID)

        if not employee.name.strip():
            errors.append(ERROR_EMPTY_NAME)

        if not EmployeeValidator._is_valid_email(employee.email):
            errors.append(ERROR_INVALID_EMAIL)

        if not employee.department.strip():
            errors.append(ERROR_EMPTY_DEPARTMENT)

        if not employee.designation.strip():
            errors.append(ERROR_EMPTY_DESIGNATION)

        if not EmployeeValidator._is_valid_date(employee.joining_date):
            errors.append(ERROR_INVALID_DATE)

        return errors

    # ── Private helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Return True if the email matches standard email format."""
        return bool(_EMAIL_REGEX.match(email.strip()))

    @staticmethod
    def _is_valid_date(date_string: str) -> bool:
        """Return True if the string is a valid date in YYYY-MM-DD format."""
        try:
            datetime.strptime(date_string.strip(), DATE_FORMAT)
            return True
        except ValueError:
            return False
