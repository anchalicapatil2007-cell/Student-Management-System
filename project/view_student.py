"""
view_student.py
----------------
This module handles displaying student records:
    - Viewing all students in a tabular format.
    - Counting the total number of students in the database.
"""

import sqlite3
from database import get_connection
from utils import print_student_table
from colors import print_error, print_info, print_header


def view_all_students():
    """
    Fetch and display all student records from the database
    in a clean tabular format.
    """
    print_header("\n----- ALL STUDENT RECORDS -----")

    select_query = "SELECT * FROM students ORDER BY id ASC"

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(select_query)
        students = cursor.fetchall()
        print_student_table(students)
    except sqlite3.Error as error:
        print_error(f"\n[ERROR] Failed to fetch students: {error}\n")
    finally:
        connection.close()


def count_students():
    """
    Display the total number of students currently stored
    in the database.
    """
    print_header("\n----- STUDENT COUNT -----")

    count_query = "SELECT COUNT(*) FROM students"

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(count_query)
        total = cursor.fetchone()[0]
        print_info(f"\n[INFO] Total number of students: {total}\n")
    except sqlite3.Error as error:
        print_error(f"\n[ERROR] Failed to count students: {error}\n")
    finally:
        connection.close()
