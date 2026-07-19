"""
File storage service.

Handles all reading and writing of employee data to/from a JSON file.
Keeping persistence logic here means no other module needs to know
where or how data is stored.
"""

import json
import os
from models.employee import Employee
from constants.app_constants import DATA_FILE_PATH


class FileStorageService:
    """Manages loading and saving employee records to a JSON file."""

    def __init__(self, file_path: str = DATA_FILE_PATH):
        self._file_path = file_path
        self._ensure_data_directory_exists()

    # ── Public interface ──────────────────────────────────────────────────────

    def load_employees(self) -> list[Employee]:
        """
        Read all employees from the JSON file.

        Returns an empty list if the file does not exist or is empty.
        Raises an IOError-derived exception if the file cannot be read.
        """
        if not os.path.exists(self._file_path):
            return []

        with open(self._file_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        return [Employee.from_dict(record) for record in raw_data]

    def save_employees(self, employees: list[Employee]) -> None:
        """
        Persist the full list of employees to the JSON file.

        Overwrites any existing data — the caller is responsible for
        passing the complete up-to-date list.
        """
        records = [emp.to_dict() for emp in employees]

        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, ensure_ascii=False)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _ensure_data_directory_exists(self) -> None:
        """Create the data directory if it does not already exist."""
        directory = os.path.dirname(self._file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
