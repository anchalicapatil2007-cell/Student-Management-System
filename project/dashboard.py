"""
dashboard.py
------------
This module displays a summary "dashboard" of statistics about the
students stored in the database — total count, breakdowns by
department/gender/semester, and average age.

This gives the console application a more professional, at-a-glance
overview, similar to a simple admin dashboard in a web app.
"""

import sqlite3
from database import get_connection
from colors import Fore, Style, print_error, print_title, print_info


def fetch_group_counts(cursor, column_name):
    """
    Run a GROUP BY query on the given column and return the results
    sorted by count (highest first).

    Args:
        cursor (sqlite3.Cursor): Active database cursor.
        column_name (str): The column to group by (e.g., 'department').

    Returns:
        list of tuples: [(value, count), ...]
    """
    # Column name is hardcoded internally (never from user input),
    # so it's safe to use directly in the query string here.
    query = f"""
        SELECT {column_name}, COUNT(*) as total
        FROM students
        GROUP BY {column_name}
        ORDER BY total DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


def print_bar_chart(rows, max_bar_length=30):
    """
    Print a simple text-based horizontal bar chart for a list of
    (label, count) rows.

    Args:
        rows (list of tuples): [(label, count), ...]
        max_bar_length (int): Maximum number of '#' characters shown
                               for the largest value.
    """
    if not rows:
        print("   (no data)")
        return

    max_count = max(count for _, count in rows)

    for label, count in rows:
        bar_length = int((count / max_count) * max_bar_length) if max_count else 0
        bar = "#" * bar_length
        print(f"   {str(label):<12} | {Fore.GREEN}{bar}{Style.RESET_ALL} "
              f"({count})")


def show_dashboard():
    """
    Display the full dashboard: total students, average age, and
    breakdowns by department, gender, and semester.
    """
    print_title("\n==============================")
    print_title("           DASHBOARD")
    print_title("==============================")

    connection = get_connection()
    try:
        cursor = connection.cursor()

        # ---- Total students ----
        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]

        if total == 0:
            print_info("\n[INFO] No student records found yet.\n")
            return

        print(f"\nTotal Students : {Fore.CYAN}{total}{Style.RESET_ALL}")

        # ---- Average age ----
        cursor.execute("SELECT AVG(age) FROM students")
        avg_age = cursor.fetchone()[0]
        print(f"Average Age    : {Fore.CYAN}{avg_age:.1f} years{Style.RESET_ALL}")

        # ---- Department-wise breakdown ----
        print("\nStudents by Department:")
        department_counts = fetch_group_counts(cursor, "department")
        print_bar_chart(department_counts)

        # ---- Gender-wise breakdown ----
        print("\nStudents by Gender:")
        gender_counts = fetch_group_counts(cursor, "gender")
        print_bar_chart(gender_counts)

        # ---- Semester-wise breakdown ----
        print("\nStudents by Semester:")
        semester_counts = fetch_group_counts(cursor, "semester")
        print_bar_chart(sorted(semester_counts, key=lambda row: row[0]))

        print()

    except sqlite3.Error as error:
        print_error(f"\n[ERROR] Could not load dashboard: {error}\n")
    finally:
        connection.close()
