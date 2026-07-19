"""
Unit tests for EmployeeValidator.

Each test method covers one rule so failures pinpoint the exact broken rule.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.employee import Employee
from validators.employee_validator import EmployeeValidator


def _make_valid_employee(**overrides) -> Employee:
    """Return a valid Employee, optionally overriding specific fields."""
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


class TestEmployeeValidator(unittest.TestCase):

    def setUp(self):
        self.validator = EmployeeValidator()

    # ── Valid case ────────────────────────────────────────────────────────────

    def test_valid_employee_returns_no_errors(self):
        employee = _make_valid_employee()
        errors = self.validator.validate(employee)
        self.assertEqual(errors, [])

    # ── Employee ID ───────────────────────────────────────────────────────────

    def test_empty_employee_id_returns_error(self):
        employee = _make_valid_employee(employee_id="")
        errors = self.validator.validate(employee)
        self.assertTrue(any("ID" in e for e in errors))

    def test_whitespace_only_employee_id_returns_error(self):
        employee = _make_valid_employee(employee_id="   ")
        errors = self.validator.validate(employee)
        self.assertTrue(any("ID" in e for e in errors))

    # ── Name ─────────────────────────────────────────────────────────────────

    def test_empty_name_returns_error(self):
        employee = _make_valid_employee(name="")
        errors = self.validator.validate(employee)
        self.assertTrue(any("Name" in e for e in errors))

    # ── Email ─────────────────────────────────────────────────────────────────

    def test_invalid_email_no_at_sign_returns_error(self):
        employee = _make_valid_employee(email="notanemail.com")
        errors = self.validator.validate(employee)
        self.assertTrue(any("Email" in e for e in errors))

    def test_invalid_email_no_domain_returns_error(self):
        employee = _make_valid_employee(email="user@")
        errors = self.validator.validate(employee)
        self.assertTrue(any("Email" in e for e in errors))

    def test_valid_email_passes(self):
        employee = _make_valid_employee(email="user.name+tag@sub.domain.co")
        errors = self.validator.validate(employee)
        self.assertFalse(any("Email" in e for e in errors))

    # ── Department ────────────────────────────────────────────────────────────

    def test_empty_department_returns_error(self):
        employee = _make_valid_employee(department="")
        errors = self.validator.validate(employee)
        self.assertTrue(any("Department" in e for e in errors))

    # ── Designation ───────────────────────────────────────────────────────────

    def test_empty_designation_returns_error(self):
        employee = _make_valid_employee(designation="")
        errors = self.validator.validate(employee)
        self.assertTrue(any("Designation" in e for e in errors))

    # ── Joining date ──────────────────────────────────────────────────────────

    def test_invalid_date_format_returns_error(self):
        employee = _make_valid_employee(joining_date="15-01-2024")
        errors = self.validator.validate(employee)
        self.assertTrue(any("date" in e.lower() for e in errors))

    def test_nonsense_date_returns_error(self):
        employee = _make_valid_employee(joining_date="not-a-date")
        errors = self.validator.validate(employee)
        self.assertTrue(any("date" in e.lower() for e in errors))

    def test_valid_date_passes(self):
        employee = _make_valid_employee(joining_date="2023-12-31")
        errors = self.validator.validate(employee)
        self.assertFalse(any("date" in e.lower() for e in errors))

    # ── Multiple errors ───────────────────────────────────────────────────────

    def test_multiple_invalid_fields_return_multiple_errors(self):
        employee = _make_valid_employee(employee_id="", name="", email="bad")
        errors = self.validator.validate(employee)
        self.assertGreaterEqual(len(errors), 3)


if __name__ == "__main__":
    unittest.main()
