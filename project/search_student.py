"""
search_student.py
------------------
This module handles searching for students by either:
    - Student ID (exact match)
    - Student Name (partial, case-insensitive match)
"""

import sqlite3
from database import get_connection
from utils import print_single_student, print_student_table
from colors import print_error, print_warning, print_header


def search_student():
    """
    Ask the user whether they want to search by ID or Name,
    then perform the search and display the results.
    """
    print_header("\n----- SEARCH STUDENT -----")
    print("1. Search by Student ID")
    print("2. Search by Student Name")
    choice = input("Enter your choice (1-2): ").strip()

    if choice == "1":
        search_by_id()
    elif choice == "2":
        search_by_name()
    else:
        print_warning("\n[INVALID] Please choose either 1 or 2.\n")


def search_by_id():
    """
    Search for a single student using their unique Student ID.
    """
    try:
        student_id = int(input("Enter Student ID: "))
    except ValueError:
        print_warning("\n[INVALID] Student ID must be a number.\n")
        return

    select_query = "SELECT * FROM students WHERE id = ?"

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(select_query, (student_id,))
        student = cursor.fetchone()
        print_single_student(student)
    except sqlite3.Error as error:
        print_error(f"\n[ERROR] Search failed: {error}\n")
    finally:
        connection.close()


def search_by_name():
    """
    Search for students whose name matches (fully or partially)
    the entered text. Case-insensitive search using SQL LIKE.
    """
    name = input("Enter Student Name (or part of it): ").strip()

    if not name:
        print_warning("\n[INVALID] Name cannot be empty.\n")
        return

    # Using LIKE with wildcards for partial matching.
    # Parameterized query still used to prevent SQL injection.
    select_query = "SELECT * FROM students WHERE name LIKE ?"
    search_pattern = f"%{name}%"

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(select_query, (search_pattern,))
        results = cursor.fetchall()

        if not results:
            print_error("\n[NOT FOUND] Student Not Found.\n")
        elif len(results) == 1:
            print_single_student(results[0])
        else:
            print_student_table(results)
    except sqlite3.Error as error:
        print_error(f"\n[ERROR] Search failed: {error}\n")
    finally:
        connection.close()
