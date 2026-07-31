"""
banner.py
---------
Displays the ASCII logo and welcome screen shown when the
application first starts, before the login prompt.

This module is purely presentational — it contains no database
or business logic, and does not affect any existing functionality.
"""

from colors import Fore, Style, print_box, print_divider

# Simple block-letter ASCII logo reading "SMS" (Student Management System).
# Kept intentionally compact so it renders cleanly on narrow terminals too.
ASCII_LOGO = r"""
 ____  __  __  ____
/ ___||  \/  |/ ___|
\___ \| |\/| |\___ \
 ___) | |  | | ___) |
|____/|_|  |_||____/
"""


def show_welcome_screen():
    """
    Display the ASCII logo and a welcome box, then wait for the user
    to press Enter before continuing to the login screen.

    Called once from main.py at program startup.
    """
    print(f"{Fore.CYAN}{Style.BRIGHT}{ASCII_LOGO}{Style.RESET_ALL}")

    print_box(
        [
            "STUDENT MANAGEMENT SYSTEM",
            "College ERP — Console Edition",
        ],
        width=44,
        color=Fore.MAGENTA,
    )

    print_divider(48, char="=", color=Fore.CYAN)
    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
