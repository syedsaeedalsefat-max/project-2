"""
utils.py - Terminal Formatting, Input Validation, and Visual Presentation Utilities.
Provides formatted banners, tables, robust validation, and ANSI color styling.
"""

import os
import sys
from typing import List, Dict, Optional, Any
from .student import Student

# Terminal ANSI Color Codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Foreground
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

    # Background
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"


def enable_windows_ansi() -> None:
    """Enable ANSI virtual terminal processing on Windows terminals if possible."""
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                mode.value |= 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
                kernel32.SetConsoleMode(handle, mode)
        except Exception:
            pass


enable_windows_ansi()


def clear_screen() -> None:
    """Clear terminal screen cross-platform."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner(title: str, subtitle: str = "") -> None:
    """Print an attractive framed header banner."""
    width = 72
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * width}{Colors.RESET}")
    print(f"{Colors.WHITE}{Colors.BOLD}{title.center(width)}{Colors.RESET}")
    if subtitle:
        print(f"{Colors.GRAY}{subtitle.center(width)}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * width}{Colors.RESET}\n")


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}--- {title} ---{Colors.RESET}")


def print_success(message: str) -> None:
    """Print a success message in green."""
    print(f"{Colors.GREEN}{Colors.BOLD}[OK]{Colors.RESET} {Colors.GREEN}{message}{Colors.RESET}")


def print_error(message: str) -> None:
    """Print an error message in red."""
    print(f"{Colors.RED}{Colors.BOLD}[ERROR]{Colors.RESET} {Colors.RED}{message}{Colors.RESET}")


def print_warning(message: str) -> None:
    """Print a warning message in yellow."""
    print(f"{Colors.YELLOW}{Colors.BOLD}[WARN]{Colors.RESET} {Colors.YELLOW}{message}{Colors.RESET}")


def print_info(message: str) -> None:
    """Print an info message in cyan."""
    print(f"{Colors.CYAN}[INFO]{Colors.RESET} {message}")


def pause(message: str = "Press Enter to return to menu...") -> None:
    """Prompt the user to press Enter to continue."""
    try:
        input(f"\n{Colors.GRAY}{message}{Colors.RESET}")
    except KeyboardInterrupt:
        print()


def prompt_string(prompt_text: str, allow_empty: bool = False) -> str:
    """
    Prompt the user for string input with empty checks.
    Returns empty string if cancelled by KeyboardInterrupt.
    """
    while True:
        try:
            value = input(f"{Colors.WHITE}{prompt_text}: {Colors.RESET}").strip()
            if not value and not allow_empty:
                print_error("Input cannot be empty. Please try again.")
                continue
            return value
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return ""


def prompt_float(prompt_text: str, min_val: float = 0.0, max_val: float = 100.0) -> Optional[float]:
    """
    Prompt user for a floating-point number within [min_val, max_val] with retries.
    Returns None if operation was cancelled via KeyboardInterrupt.
    """
    while True:
        try:
            raw = input(f"{Colors.WHITE}{prompt_text} ({min_val:g}-{max_val:g}): {Colors.RESET}").strip()
            val = float(raw)
            if val < min_val or val > max_val:
                print_error(f"Value must be between {min_val} and {max_val}. Got: {val}")
                continue
            return val
        except ValueError:
            print_error("Invalid number! Please enter a valid decimal or integer value.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None


def render_student_table(students: List[Student]) -> None:
    """
    Render a clean tabular view of multiple students.
    """
    if not students:
        print_warning("No student records found to display.")
        return

    # Table layout
    header_fmt = (
        f"{Colors.BOLD}{Colors.WHITE}"
        f" {'#':<3} {'ID':<8} {'Name':<18} "
        f"{'Math':<5} {'Phys':<5} {'Chem':<5} {'Eng':<5} {'CS':<5} "
        f"{'Total':<7} {'Pct':<7} {'Grd':<4} {'Status':<6}"
        f"{Colors.RESET}"
    )
    divider = "-" * 88

    print(f"{Colors.CYAN}{divider}{Colors.RESET}")
    print(header_fmt)
    print(f"{Colors.CYAN}{divider}{Colors.RESET}")

    for idx, s in enumerate(students, 1):
        m = s.marks
        status_color = Colors.GREEN if s.status == "PASS" else Colors.RED
        row = (
            f" {idx:<3} {s.student_id:<8} {s.name[:16]:<18} "
            f"{m.get('Mathematics', 0):>4.0f}  "
            f"{m.get('Physics', 0):>4.0f}  "
            f"{m.get('Chemistry', 0):>4.0f}  "
            f"{m.get('English', 0):>4.0f}  "
            f"{m.get('Computer Science', 0):>4.0f}  "
            f"{s.total_marks:>6.1f}  "
            f"{s.percentage:>5.1f}% "
            f"{s.grade:^4} "
            f"{status_color}{s.status:^6}{Colors.RESET}"
        )
        print(row)

    print(f"{Colors.CYAN}{divider}{Colors.RESET}")
    print(f" Total records displayed: {len(students)}")

