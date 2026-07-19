"""
Employee service.

Contains all business logic for managing employees.
This class does not know about the console or how data is displayed —
that separation makes the logic independently testable.
"""

from models.employee import Employee
from validators.employee_validator import EmployeeValidator
from services.file_storage_service import FileStorageService
from constants.app_constants import (
    MSG_EMPLOYEE_NOT_FOUND,
    MSG_DUPLICATE_ID,
)


class EmployeeService:
    """Provides CRUD operations and query methods for employees."""

    def __init__(self, storage: FileStorageService = None):
        # Allow dependency injection so unit tests can pass a mock storage
        self._storage = storage or FileStorageService()
        self._employees: list[Employee] = self._storage.load_employees()
        self._validator = EmployeeValidator()

    # ── Create ────────────────────────────────────────────────────────────────

    def add_employee(self, employee: Employee) -> tuple[bool, list[str]]:
        """
        Validate and add a new employee.

        Returns:
            (True, []) on success.
            (False, [error messages]) on validation failure or duplicate ID.
        """
        errors = self._validator.validate(employee)
        if errors:
            return False, errors

        if self._id_exists(employee.employee_id):
            return False, [MSG_DUPLICATE_ID]

        self._employees.append(employee)
        self._persist()
        return True, []

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_all_employees(self) -> list[Employee]:
        """Return all employees in the order they were added."""
        return list(self._employees)

    def get_employee_by_id(self, employee_id: str) -> Employee | None:
        """Return the employee with the given ID, or None if not found."""
        target_id = employee_id.strip().upper()
        for employee in self._employees:
            if employee.employee_id.upper() == target_id:
                return employee
        return None

    def get_employees_sorted_by_name(self) -> list[Employee]:
        """Return all employees sorted alphabetically by name (case-insensitive)."""
        return sorted(self._employees, key=lambda emp: emp.name.lower())

    def get_employees_by_department(self, department: str) -> list[Employee]:
        """Return employees whose department matches the given name (case-insensitive)."""
        target = department.strip().lower()
        return [emp for emp in self._employees if emp.department.lower() == target]

    # ── Update ────────────────────────────────────────────────────────────────

    def update_employee(self, employee_id: str, updated_employee: Employee) -> tuple[bool, list[str]]:
        """
        Replace the data of an existing employee.

        Returns:
            (True, []) on success.
            (False, [error messages]) if not found or validation fails.
        """
        errors = self._validator.validate(updated_employee)
        if errors:
            return False, errors

        for index, employee in enumerate(self._employees):
            if employee.employee_id.upper() == employee_id.strip().upper():
                self._employees[index] = updated_employee
                self._persist()
                return True, []

        return False, [MSG_EMPLOYEE_NOT_FOUND]

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete_employee(self, employee_id: str) -> tuple[bool, str]:
        """
        Remove the employee with the given ID.

        Returns:
            (True, success_message) or (False, error_message).
        """
        target_id = employee_id.strip().upper()
        for index, employee in enumerate(self._employees):
            if employee.employee_id.upper() == target_id:
                self._employees.pop(index)
                self._persist()
                return True, f"Employee '{employee.name}' deleted successfully."

        return False, MSG_EMPLOYEE_NOT_FOUND

    # ── Private helpers ───────────────────────────────────────────────────────

    def _id_exists(self, employee_id: str) -> bool:
        """Check whether an employee with this ID already exists."""
        target = employee_id.strip().upper()
        return any(emp.employee_id.upper() == target for emp in self._employees)

    def _persist(self) -> None:
        """Save the current in-memory list to storage."""
        self._storage.save_employees(self._employees)
