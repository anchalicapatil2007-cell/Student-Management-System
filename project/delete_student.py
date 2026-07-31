"""
delete_student.py
------------------
This module handles deleting a student record from the database
using the Student ID. A confirmation prompt is shown before
deletion to prevent accidental data loss.
"""

import sqlite3
from database import get_connection
from utils import print_single_student
from colors import print_success, print_error, print_warning, print_header


def delete_student():
    """
    Delete a student record after confirming with the user.
    """
    print_header("\n----- DELETE STUDENT -----")

    try:
        student_id = int(input("Enter Student ID to delete: "))
    except ValueError:
        print_warning("\n[INVALID] Student ID must be a number.\n")
        return

    connection = get_connection()
    try:
        cursor = connection.cursor()

        # First, check whether the student exists.
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()

        if not student:
            print_error("\n[NOT FOUND] Student Not Found.\n")
            return

        print("\nStudent to be deleted:")
        print_single_student(student)

        # ---- Confirmation before deleting ----
        confirmation = input(
            "Are you sure you want to delete this student? (yes/no): "
        ).strip().lower()

        if confirmation not in ("yes", "y"):
            print_warning("\n[CANCELLED] Deletion cancelled.\n")
            return

        # ---- Delete using a parameterized query ----
        delete_query = "DELETE FROM students WHERE id = ?"
        cursor.execute(delete_query, (student_id,))
        connection.commit()
        print_success(f"\n[SUCCESS] Student ID {student_id} deleted successfully.\n")

    except sqlite3.Error as error:
        print_error(f"\n[ERROR] Deletion failed: {error}\n")
    finally:
        connection.close()
