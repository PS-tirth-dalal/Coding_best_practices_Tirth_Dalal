"""
Unit tests for EmployeeService.

Uses an in-memory mock storage so tests never touch the filesystem.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.employee import Employee
from services.employee_service import EmployeeService


class _InMemoryStorage:
    """Fake storage that keeps employees in a list — no file I/O."""

    def __init__(self, initial_employees: list[Employee] = None):
        self._data = list(initial_employees or [])

    def load_employees(self) -> list[Employee]:
        return list(self._data)

    def save_employees(self, employees: list[Employee]) -> None:
        self._data = list(employees)


def _make_employee(**overrides) -> Employee:
    """Return a valid Employee with sensible defaults."""
    defaults = {
        "employee_id":  "EMP001",
        "name":         "Alice Smith",
        "email":        "alice@example.com",
        "department":   "Engineering",
        "designation":  "Software Engineer",
        "joining_date": "2024-01-15",
    }
    defaults.update(overrides)
    return Employee(**defaults)


class TestEmployeeServiceAdd(unittest.TestCase):

    def setUp(self):
        self.service = EmployeeService(storage=_InMemoryStorage())

    def test_add_valid_employee_succeeds(self):
        success, errors = self.service.add_employee(_make_employee())
        self.assertTrue(success)
        self.assertEqual(errors, [])

    def test_added_employee_appears_in_list(self):
        self.service.add_employee(_make_employee())
        employees = self.service.get_all_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0].employee_id, "EMP001")

    def test_add_duplicate_id_returns_error(self):
        self.service.add_employee(_make_employee())
        success, errors = self.service.add_employee(_make_employee())
        self.assertFalse(success)
        self.assertTrue(len(errors) > 0)

    def test_add_invalid_employee_returns_errors(self):
        bad_employee = _make_employee(email="not-an-email", name="")
        success, errors = self.service.add_employee(bad_employee)
        self.assertFalse(success)
        self.assertGreater(len(errors), 0)


class TestEmployeeServiceRead(unittest.TestCase):

    def setUp(self):
        emp1 = _make_employee(employee_id="EMP001", name="Charlie Brown", department="HR")
        emp2 = _make_employee(employee_id="EMP002", name="Alice Smith", department="Engineering")
        emp3 = _make_employee(employee_id="EMP003", name="Bob Jones", department="Engineering", email="bob@example.com")
        self.service = EmployeeService(storage=_InMemoryStorage([emp1, emp2, emp3]))

    def test_get_all_returns_all_employees(self):
        self.assertEqual(len(self.service.get_all_employees()), 3)

    def test_get_by_id_found(self):
        emp = self.service.get_employee_by_id("EMP002")
        self.assertIsNotNone(emp)
        self.assertEqual(emp.name, "Alice Smith")

    def test_get_by_id_case_insensitive(self):
        emp = self.service.get_employee_by_id("emp002")
        self.assertIsNotNone(emp)

    def test_get_by_id_not_found_returns_none(self):
        emp = self.service.get_employee_by_id("EMP999")
        self.assertIsNone(emp)

    def test_sort_by_name_returns_alphabetical_order(self):
        sorted_employees = self.service.get_employees_sorted_by_name()
        names = [e.name for e in sorted_employees]
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_filter_by_department_returns_correct_employees(self):
        engineering = self.service.get_employees_by_department("Engineering")
        self.assertEqual(len(engineering), 2)

    def test_filter_by_department_case_insensitive(self):
        engineering = self.service.get_employees_by_department("engineering")
        self.assertEqual(len(engineering), 2)

    def test_filter_nonexistent_department_returns_empty_list(self):
        result = self.service.get_employees_by_department("Marketing")
        self.assertEqual(result, [])


class TestEmployeeServiceUpdate(unittest.TestCase):

    def setUp(self):
        emp = _make_employee(employee_id="EMP001", name="Alice Smith")
        self.service = EmployeeService(storage=_InMemoryStorage([emp]))

    def test_update_existing_employee_succeeds(self):
        updated = _make_employee(employee_id="EMP001", name="Alice Johnson")
        success, errors = self.service.update_employee("EMP001", updated)
        self.assertTrue(success)
        self.assertEqual(self.service.get_employee_by_id("EMP001").name, "Alice Johnson")

    def test_update_nonexistent_employee_returns_error(self):
        updated = _make_employee(employee_id="EMP999")
        success, errors = self.service.update_employee("EMP999", updated)
        self.assertFalse(success)

    def test_update_with_invalid_data_returns_errors(self):
        bad = _make_employee(employee_id="EMP001", email="bad-email")
        success, errors = self.service.update_employee("EMP001", bad)
        self.assertFalse(success)
        self.assertGreater(len(errors), 0)


class TestEmployeeServiceDelete(unittest.TestCase):

    def setUp(self):
        emp = _make_employee(employee_id="EMP001", name="Alice Smith")
        self.service = EmployeeService(storage=_InMemoryStorage([emp]))

    def test_delete_existing_employee_succeeds(self):
        success, _ = self.service.delete_employee("EMP001")
        self.assertTrue(success)
        self.assertIsNone(self.service.get_employee_by_id("EMP001"))

    def test_delete_reduces_employee_count(self):
        self.service.delete_employee("EMP001")
        self.assertEqual(len(self.service.get_all_employees()), 0)

    def test_delete_nonexistent_employee_returns_error(self):
        success, message = self.service.delete_employee("EMP999")
        self.assertFalse(success)
        self.assertIn("no employee found", message.lower())


if __name__ == "__main__":
    unittest.main()
