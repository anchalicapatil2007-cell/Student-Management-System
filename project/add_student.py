"""
add_student.py
---------------
This module handles adding a new student record to the database.

It collects and validates user input, then inserts the record
into the 'students' table using a parameterized SQL query
(to prevent SQL injection).

Age is calculated automatically from the entered Date of Birth,
so the two fields can never contradict each other.
"""

import sqlite3
from database import get_connection
from colors import print_success, print_error
from utils import (
    get_valid_str,
    get_valid_date,
    validate_name,
    validate_age,
    validate_phone,
    validate_email,
    validate_semester,
    validate_gender,
    validate_photo_path,
    calculate_age_from_dob,
)


def add_student():
    """
    Prompt the user for student details, validate the input,
    and insert a new record into the students table.
    """
    print("\n----- ADD NEW STUDENT -----")

    # ---- Collect and validate input ----
    name = get_valid_str(
        "Enter Name: ",
        validate_name,
        "Name cannot be empty."
    )

    # Date of Birth drives the age calculation, so age is never
    # entered inconsistently with the birth date.
    while True:
        dob = get_valid_date("Enter Date of Birth (YYYY-MM-DD): ")
        age = calculate_age_from_dob(dob)
        if validate_age(age):
            break
        print(f"[INVALID] Calculated age is {age}, but age must be "
              f"between 16 and 35. Please re-enter Date of Birth.")

    gender = get_valid_str(
        "Enter Gender (Male/Female/Other): ",
        validate_gender,
        "Gender must be Male, Female, or Other."
    ).capitalize()

    department = get_valid_str(
        "Enter Department (e.g., AIDS, CSE, MECH): ",
        validate_name,
        "Department cannot be empty."
    )

    semester = int(get_valid_str(
        "Enter Semester (1-8): ",
        lambda v: v.isdigit() and validate_semester(int(v)),
        "Semester must be a whole number between 1 and 8."
    ))

    phone = get_valid_str(
        "Enter Phone Number (10 digits): ",
        validate_phone,
        "Phone number must contain exactly 10 digits."
    )

    email = get_valid_str(
        "Enter Email: ",
        validate_email,
        "Please enter a valid email address (e.g., name@example.com)."
    )

    address = get_valid_str(
        "Enter Address: ",
        validate_name,
        "Address cannot be empty."
    )

    photo_path = get_valid_str(
        "Enter Photo File Path (optional, press Enter to skip): ",
        validate_photo_path,
        "This field is optional."
    )
    photo_path = photo_path if photo_path else "N/A"

    admission_date = get_valid_date(
        "Enter Admission Date (YYYY-MM-DD, press Enter for today): ",
        allow_blank_for_today=True
    )

    # ---- Insert into database using a parameterized query ----
    insert_query = """
        INSERT INTO students
            (name, dob, age, gender, department, semester,
             phone, email, address, photo_path, admission_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            insert_query,
            (name, dob, age, gender, department, semester,
             phone, email, address, photo_path, admission_date)
        )
        connection.commit()
        print_success(f"\n[SUCCESS] Student '{name}' added successfully "
                      f"with ID {cursor.lastrowid}.\n")
    except sqlite3.Error as error:
        print_error(f"\n[ERROR] Failed to add student: {error}\n")
    finally:
        connection.close()
