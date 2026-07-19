"""
Employee model.

Represents a single employee record. Using a dataclass keeps the
definition concise while giving us __repr__, __eq__, and type clarity for free.
"""

from dataclasses import dataclass, field
from datetime import datetime
from constants.app_constants import DATE_FORMAT, DATE_FORMAT_DISPLAY


@dataclass
class Employee:
    """Holds all details for a single employee."""

    employee_id: str
    name: str
    email: str
    department: str
    designation: str
    joining_date: str   # Stored as ISO string "YYYY-MM-DD" for easy JSON serialisation

    # ── Serialisation helpers ─────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Convert this employee to a plain dictionary (for JSON storage)."""
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "designation": self.designation,
            "joining_date": self.joining_date,
        }

    @staticmethod
    def from_dict(data: dict) -> "Employee":
        """Create an Employee instance from a dictionary (loaded from JSON)."""
        return Employee(
            employee_id=data["employee_id"],
            name=data["name"],
            email=data["email"],
            department=data["department"],
            designation=data["designation"],
            joining_date=data["joining_date"],
        )

    # ── Display helper ────────────────────────────────────────────────────────

    def formatted_joining_date(self) -> str:
        """Return the joining date in a human-readable format (e.g. 15 Jan 2024)."""
        try:
            date_obj = datetime.strptime(self.joining_date, DATE_FORMAT)
            return date_obj.strftime(DATE_FORMAT_DISPLAY)
        except ValueError:
            return self.joining_date  # Fall back to raw string if format is unexpected
