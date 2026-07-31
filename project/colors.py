"""
colors.py
---------
Centralized helpers for colored terminal output.

Uses the 'colorama' package for cross-platform ANSI colors
(works on Windows, macOS, and Linux terminals).

If colorama is not installed, the program still works normally —
it just falls back to plain, uncolored text instead of crashing.
"""

try:
    from colorama import Fore, Style, init
    # Automatically resets color after each print() and enables
    # ANSI colors on Windows terminals.
    init(autoreset=True)
    COLOR_AVAILABLE = True
except ImportError:
    COLOR_AVAILABLE = False

    # Dummy replacements so the rest of the code doesn't break
    # if colorama isn't installed.
    class _DummyColor:
        def __getattr__(self, name):
            return ""

    Fore = _DummyColor()
    Style = _DummyColor()


def print_success(message):
    """Print a success message in green."""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


def print_error(message):
    """Print an error message in red."""
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def print_warning(message):
    """Print a warning message in yellow."""
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")


def print_info(message):
    """Print an informational message in cyan."""
    print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")


def print_header(message):
    """Print a bold section header in blue."""
    print(f"{Fore.BLUE}{Style.BRIGHT}{message}{Style.RESET_ALL}")


def print_title(message):
    """Print a bright magenta title (used for the main banner)."""
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{message}{Style.RESET_ALL}")


def print_divider(width=60, char="─", color=None):
    """
    Print a horizontal divider line.

    Args:
        width (int): Number of characters in the line.
        char (str): Character used to draw the line.
        color: A colorama Fore.* color to apply (defaults to cyan).
    """
    line_color = color if color is not None else Fore.CYAN
    print(f"{line_color}{char * width}{Style.RESET_ALL}")


def print_box(lines, width=60, color=None):
    """
    Print a list of text lines inside a simple box-drawing border.
    Each line is centered within the box. Used for banners, welcome
    screens, and short summary panels.

    Args:
        lines (list of str): The lines of text to display inside the box.
        width (int): Total inner width of the box (excluding borders).
        color: A colorama Fore.* color to apply to the border
               (defaults to cyan).
    """
    box_color = color if color is not None else Fore.CYAN

    top_border = f"{box_color}┌{'─' * (width + 2)}┐{Style.RESET_ALL}"
    bottom_border = f"{box_color}└{'─' * (width + 2)}┘{Style.RESET_ALL}"

    print(top_border)
    for line in lines:
        centered_line = line.center(width)
        print(f"{box_color}│ {Style.RESET_ALL}{centered_line}"
              f"{box_color} │{Style.RESET_ALL}")
    print(bottom_border)
