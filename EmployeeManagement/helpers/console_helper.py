"""
Console helper.

All console display logic lives here — colours, tables, banners, and
user prompts. Keeping this separate from business logic means the
look of the app can change without touching any service code.
"""

from models.employee import Employee


# ── ANSI colour codes ─────────────────────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"


class ConsoleHelper:
    """Utility class for all console input/output operations."""

    # ── Banner & Menu ─────────────────────────────────────────────────────────

    @staticmethod
    def print_banner() -> None:
        """Display the application title banner."""
        print(f"\n{Color.CYAN}{Color.BOLD}")
        print("╔══════════════════════════════════════════════════╗")
        print("║        EMPLOYEE MANAGEMENT SYSTEM                ║")
        print("╚══════════════════════════════════════════════════╝")
        print(Color.RESET)

    @staticmethod
    def print_menu() -> None:
        """Display the main navigation menu."""
        print(f"\n{Color.BOLD}{Color.WHITE}┌─────────────────────────────────┐")
        print("│           MAIN MENU             │")
        print("├─────────────────────────────────┤")
        print("│  1. Add Employee                │")
        print("│  2. View All Employees          │")
        print("│  3. Search Employee by ID       │")
        print("│  4. Update Employee             │")
        print("│  5. Delete Employee             │")
        print("│  6. Sort Employees by Name      │")
        print("│  7. Filter by Department        │")
        print("│  8. Exit                        │")
        print("└─────────────────────────────────┘")
        print(Color.RESET, end="")

    # ── Message helpers ───────────────────────────────────────────────────────

    @staticmethod
    def print_success(message: str) -> None:
        """Print a success message in green."""
        print(f"\n{Color.GREEN}✔  {message}{Color.RESET}")

    @staticmethod
    def print_error(message: str) -> None:
        """Print an error message in red."""
        print(f"\n{Color.RED}✘  {message}{Color.RESET}")

    @staticmethod
    def print_info(message: str) -> None:
        """Print an informational message in yellow."""
        print(f"\n{Color.YELLOW}ℹ  {message}{Color.RESET}")

    @staticmethod
    def print_errors(errors: list[str]) -> None:
        """Print a numbered list of validation errors."""
        print(f"\n{Color.RED}The following errors were found:{Color.RESET}")
        for i, error in enumerate(errors, start=1):
            print(f"  {Color.RED}{i}. {error}{Color.RESET}")

    @staticmethod
    def print_section_header(title: str) -> None:
        """Print a section heading."""
        print(f"\n{Color.BLUE}{Color.BOLD}── {title} {'─' * (45 - len(title))}{Color.RESET}")

    # ── Employee display ──────────────────────────────────────────────────────

    @staticmethod
    def print_employee_table(employees: list[Employee]) -> None:
        """Render a formatted table of employees."""
        if not employees:
            ConsoleHelper.print_info("No employee records to display.")
            return

        col_widths = {"id": 10, "name": 20, "email": 28, "dept": 16, "desig": 18, "date": 14}

        # Header row
        header = (
            f"{'ID':<{col_widths['id']}} "
            f"{'Name':<{col_widths['name']}} "
            f"{'Email':<{col_widths['email']}} "
            f"{'Department':<{col_widths['dept']}} "
            f"{'Designation':<{col_widths['desig']}} "
            f"{'Joining Date':<{col_widths['date']}}"
        )
        separator = "─" * len(header)

        print(f"\n{Color.CYAN}{Color.BOLD}{header}{Color.RESET}")
        print(f"{Color.CYAN}{separator}{Color.RESET}")

        # Data rows — alternate subtle styling for readability
        for employee in employees:
            row = (
                f"{employee.employee_id:<{col_widths['id']}} "
                f"{employee.name:<{col_widths['name']}} "
                f"{employee.email:<{col_widths['email']}} "
                f"{employee.department:<{col_widths['dept']}} "
                f"{employee.designation:<{col_widths['desig']}} "
                f"{employee.formatted_joining_date():<{col_widths['date']}}"
            )
            print(row)

        print(f"{Color.CYAN}{separator}{Color.RESET}")
        print(f"{Color.YELLOW}Total: {len(employees)} employee(s){Color.RESET}\n")

    @staticmethod
    def print_employee_detail(employee: Employee) -> None:
        """Display full details of a single employee in a card-style layout."""
        print(f"\n{Color.CYAN}{Color.BOLD}{'─' * 45}{Color.RESET}")
        print(f"  {Color.BOLD}Employee ID  :{Color.RESET} {employee.employee_id}")
        print(f"  {Color.BOLD}Name         :{Color.RESET} {employee.name}")
        print(f"  {Color.BOLD}Email        :{Color.RESET} {employee.email}")
        print(f"  {Color.BOLD}Department   :{Color.RESET} {employee.department}")
        print(f"  {Color.BOLD}Designation  :{Color.RESET} {employee.designation}")
        print(f"  {Color.BOLD}Joining Date :{Color.RESET} {employee.formatted_joining_date()}")
        print(f"{Color.CYAN}{Color.BOLD}{'─' * 45}{Color.RESET}")

    # ── Input prompts ─────────────────────────────────────────────────────────

    @staticmethod
    def prompt(label: str) -> str:
        """Prompt the user for a string value and return the stripped input."""
        return input(f"  {Color.MAGENTA}{label}: {Color.RESET}").strip()

    @staticmethod
    def prompt_with_default(label: str, current_value: str) -> str:
        """
        Prompt the user for input; if they press Enter, keep the current value.
        Useful for partial updates where only some fields need to change.
        """
        user_input = input(
            f"  {Color.MAGENTA}{label} [{Color.YELLOW}{current_value}{Color.MAGENTA}]: {Color.RESET}"
        ).strip()
        return user_input if user_input else current_value

    @staticmethod
    def confirm(message: str) -> bool:
        """Ask a yes/no question; return True if the user answers yes."""
        answer = input(f"\n  {Color.YELLOW}{message} (y/n): {Color.RESET}").strip().lower()
        return answer == "y"

    @staticmethod
    def press_enter_to_continue() -> None:
        """Pause until the user presses Enter."""
        input(f"\n  {Color.WHITE}Press Enter to continue...{Color.RESET}")
