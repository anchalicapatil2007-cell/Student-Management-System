"""
main.py
-------
Entry point of the Student Management System.

This script:
    1. Initializes the SQLite database (creates it if missing).
    2. Requires an admin to log in before granting access.
    3. Displays the main menu.
    4. Routes the user's choice to the appropriate module/function.

Run this file to start the application:
    python main.py
"""

from database import initialize_database
from auth import login_screen, change_password
from banner import show_welcome_screen
from add_student import add_student
from view_student import view_all_students, count_students
from search_student import search_student
from update_student import update_student
from delete_student import delete_student
from export_data import export_to_csv
from dashboard import show_dashboard
from colors import Fore, Style, print_title, print_warning


def display_menu(username):
    """Print the main menu options to the console."""
    print_title("\n==============================")
    print_title(" STUDENT MANAGEMENT SYSTEM")
    print(f"{Fore.MAGENTA}     Logged in as: {username}{Style.RESET_ALL}")
    print_title("==============================")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Count Students")
    print("7. Dashboard")
    print("8. Export to CSV")
    print("9. Change Password")
    print("10. Logout / Exit")
    print_title("==============================")


def main():
    """
    Main application loop.
    Initializes the database, requires login, then repeatedly shows
    the menu and dispatches user choices until the user exits.
    """
    # ---- Show the welcome screen / ASCII logo first ----
    show_welcome_screen()

    # Ensure the database and tables exist before doing anything else.
    initialize_database()

    # ---- Require login before granting access to the system ----
    username = login_screen()
    if username is None:
        return  # Too many failed attempts — exit the program.

    # Map each menu choice to its corresponding function.
    # This avoids a long chain of if-elif statements.
    menu_actions = {
        "1": add_student,
        "2": view_all_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "6": count_students,
        "7": show_dashboard,
        "8": export_to_csv,
    }

    while True:
        display_menu(username)
        choice = input("Enter your choice (1-10): ").strip()

        if choice == "10":
            print("\nThank you for using the Student Management System. Goodbye!\n")
            break
        elif choice == "9":
            change_password(username)
        else:
            action = menu_actions.get(choice)
            if action:
                try:
                    action()
                except Exception as error:
                    # Catch-all safety net so an unexpected error doesn't
                    # crash the whole application.
                    print(f"\n[UNEXPECTED ERROR] {error}\n")
            else:
                print_warning("\n[INVALID] Please enter a number between 1 and 10.\n")


# Standard Python entry-point guard.
# Ensures main() only runs when this file is executed directly,
# not when it's imported as a module elsewhere.
if __name__ == "__main__":
    main()
