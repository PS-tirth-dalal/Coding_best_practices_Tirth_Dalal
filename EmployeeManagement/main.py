"""
Main entry point for the Employee Management System.

This module contains the menu-driven interaction loop.
It delegates all business logic to EmployeeService and all display
work to ConsoleHelper — keeping this file focused on orchestration only.
"""

import os
import sys

# Allow imports from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.employee import Employee
from services.employee_service import EmployeeService
from helpers.console_helper import ConsoleHelper
from constants.app_constants import (
    MENU_ADD_EMPLOYEE,
    MENU_VIEW_ALL_EMPLOYEES,
    MENU_SEARCH_EMPLOYEE,
    MENU_UPDATE_EMPLOYEE,
    MENU_DELETE_EMPLOYEE,
    MENU_SORT_BY_NAME,
    MENU_FILTER_BY_DEPT,
    MENU_EXIT,
    MSG_INVALID_CHOICE,
    MSG_GOODBYE,
    MSG_EMPLOYEE_NOT_FOUND,
)


def add_employee(service: EmployeeService) -> None:
    """Collect employee details from the user and add to the system."""
    ConsoleHelper.print_section_header("Add New Employee")

    employee = Employee(
        employee_id  = ConsoleHelper.prompt("Employee ID"),
        name         = ConsoleHelper.prompt("Full Name"),
        email        = ConsoleHelper.prompt("Email Address"),
        department   = ConsoleHelper.prompt("Department"),
        designation  = ConsoleHelper.prompt("Designation"),
        joining_date = ConsoleHelper.prompt("Joining Date (YYYY-MM-DD)"),
    )

    success, errors = service.add_employee(employee)

    if success:
        ConsoleHelper.print_success("Employee added successfully.")
    else:
        ConsoleHelper.print_errors(errors)


def view_all_employees(service: EmployeeService) -> None:
    """Display all employees in a formatted table."""
    ConsoleHelper.print_section_header("All Employees")
    employees = service.get_all_employees()
    ConsoleHelper.print_employee_table(employees)


def search_employee(service: EmployeeService) -> None:
    """Search for an employee by ID and display their details."""
    ConsoleHelper.print_section_header("Search Employee by ID")
    employee_id = ConsoleHelper.prompt("Enter Employee ID")

    employee = service.get_employee_by_id(employee_id)

    if employee:
        ConsoleHelper.print_employee_detail(employee)
    else:
        ConsoleHelper.print_error(MSG_EMPLOYEE_NOT_FOUND)


def update_employee(service: EmployeeService) -> None:
    """Update an existing employee's details, keeping unchanged fields intact."""
    ConsoleHelper.print_section_header("Update Employee")
    employee_id = ConsoleHelper.prompt("Enter Employee ID to update")

    existing = service.get_employee_by_id(employee_id)
    if not existing:
        ConsoleHelper.print_error(MSG_EMPLOYEE_NOT_FOUND)
        return

    ConsoleHelper.print_info("Press Enter to keep the current value for any field.")

    updated_employee = Employee(
        employee_id  = existing.employee_id,   # ID cannot be changed
        name         = ConsoleHelper.prompt_with_default("Full Name", existing.name),
        email        = ConsoleHelper.prompt_with_default("Email Address", existing.email),
        department   = ConsoleHelper.prompt_with_default("Department", existing.department),
        designation  = ConsoleHelper.prompt_with_default("Designation", existing.designation),
        joining_date = ConsoleHelper.prompt_with_default("Joining Date (YYYY-MM-DD)", existing.joining_date),
    )

    success, errors = service.update_employee(employee_id, updated_employee)

    if success:
        ConsoleHelper.print_success("Employee updated successfully.")
    else:
        ConsoleHelper.print_errors(errors)


def delete_employee(service: EmployeeService) -> None:
    """Delete an employee after user confirmation."""
    ConsoleHelper.print_section_header("Delete Employee")
    employee_id = ConsoleHelper.prompt("Enter Employee ID to delete")

    existing = service.get_employee_by_id(employee_id)
    if not existing:
        ConsoleHelper.print_error(MSG_EMPLOYEE_NOT_FOUND)
        return

    ConsoleHelper.print_employee_detail(existing)

    if ConsoleHelper.confirm(f"Are you sure you want to delete '{existing.name}'?"):
        success, message = service.delete_employee(employee_id)
        if success:
            ConsoleHelper.print_success(message)
        else:
            ConsoleHelper.print_error(message)
    else:
        ConsoleHelper.print_info("Delete operation cancelled.")


def sort_employees_by_name(service: EmployeeService) -> None:
    """Display all employees sorted alphabetically by name."""
    ConsoleHelper.print_section_header("Employees Sorted by Name")
    employees = service.get_employees_sorted_by_name()
    ConsoleHelper.print_employee_table(employees)


def filter_by_department(service: EmployeeService) -> None:
    """Display employees filtered by a chosen department."""
    ConsoleHelper.print_section_header("Filter by Department")
    department = ConsoleHelper.prompt("Enter Department name")

    employees = service.get_employees_by_department(department)

    if employees:
        ConsoleHelper.print_employee_table(employees)
    else:
        ConsoleHelper.print_info(f"No employees found in the '{department}' department.")


# Maps each menu choice string to the corresponding handler function.
# Adding a new menu option only requires adding an entry here — no if/elif chain needed.
MENU_HANDLERS = {
    MENU_ADD_EMPLOYEE:       add_employee,
    MENU_VIEW_ALL_EMPLOYEES: view_all_employees,
    MENU_SEARCH_EMPLOYEE:    search_employee,
    MENU_UPDATE_EMPLOYEE:    update_employee,
    MENU_DELETE_EMPLOYEE:    delete_employee,
    MENU_SORT_BY_NAME:       sort_employees_by_name,
    MENU_FILTER_BY_DEPT:     filter_by_department,
}


def run() -> None:
    """Start the application and run the main menu loop."""
    service = EmployeeService()
    ConsoleHelper.print_banner()

    while True:
        ConsoleHelper.print_menu()
        choice = ConsoleHelper.prompt("Select an option")

        if choice == MENU_EXIT:
            ConsoleHelper.print_success(MSG_GOODBYE)
            break

        handler = MENU_HANDLERS.get(choice)
        if handler:
            try:
                handler(service)
            except Exception as error:
                # Catch unexpected errors gracefully so the app never crashes
                ConsoleHelper.print_error(f"An unexpected error occurred: {error}")
        else:
            ConsoleHelper.print_error(MSG_INVALID_CHOICE)

        ConsoleHelper.press_enter_to_continue()


if __name__ == "__main__":
    run()
