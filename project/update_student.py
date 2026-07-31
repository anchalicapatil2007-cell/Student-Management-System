"""
update_student.py
------------------
This module handles updating an existing student's details
using their Student ID.

The current details are shown first, and the user can choose
to keep or change each field individually. If the Date of Birth
is changed, the Age field is automatically recalculated to keep
the two fields consistent.
"""

import sqlite3
from database import get_connection
from colors import print_success, print_error, print_warning, print_header
from utils import (
    print_single_student,
    validate_name,
    validate_age,
    validate_phone,
    validate_email,
    validate_semester,
    validate_gender,
    validate_date_format,
    calculate_age_from_dob,
)


def get_student_by_id(cursor, student_id):
    """Fetch a single student record by ID."""
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    return cursor.fetchone()


def prompt_new_value(field_label, current_value, validator, error_message,
                      cast_type=str):
    """
    Prompt the user to either keep the current value (by pressing Enter)
    or provide a new validated value.
    """
    while True:
        new_value = input(
            f"{field_label} [{current_value}] (press Enter to keep): "
        ).strip()

        if new_value == "":
            return current_value

        try:
            casted_value = cast_type(new_value)
        except ValueError:
            print(f"[INVALID] Please enter a valid {cast_type.__name__}.")
            continue

        if validator(casted_value):
            return casted_value
        print(f"[INVALID] {error_message}")


def update_student():
    """
    Update an existing student's record.
    Shows current details, then lets the user update each field.
    """
    print_header("\n----- UPDATE STUDENT -----")

    try:
        student_id = int(input("Enter Student ID to update: "))
    except ValueError:
        print_warning("\n[INVALID] Student ID must be a number.\n")
        return

    connection = get_connection()
    try:
        cursor = connection.cursor()
        student = get_student_by_id(cursor, student_id)

        if not student:
            print_error("\n[NOT FOUND] Student Not Found.\n")
            return

        print("\nCurrent Details:")
        print_single_student(student)

        (current_id, current_name, current_dob, current_age,
         current_gender, current_department, current_semester,
         current_phone, current_email, current_address,
         current_photo_path, current_admission_date) = student

        print("Enter new values below, or press Enter to keep the current value.\n")

        # ---- Collect updated values (with validation) ----
        name = prompt_new_value(
            "Name", current_name, validate_name, "Name cannot be empty.", str
        )

        dob = prompt_new_value(
            "Date of Birth (YYYY-MM-DD)", current_dob, validate_date_format,
            "Date must be a valid YYYY-MM-DD date, not in the future.", str
        )
        # Recalculate age automatically whenever DOB changes, so the
        # two fields never contradict each other.
        age = calculate_age_from_dob(dob) if dob != current_dob else current_age
        if not validate_age(age):
            print_warning(
                f"[WARNING] Age calculated from new DOB is {age}, which is "
                f"outside the allowed 16-35 range. Keeping previous DOB/Age."
            )
            dob, age = current_dob, current_age

        gender_input = prompt_new_value(
            "Gender", current_gender, validate_gender,
            "Gender must be Male, Female, or Other.", str
        )
        gender = gender_input.capitalize()

        department = prompt_new_value(
            "Department", current_department, validate_name,
            "Department cannot be empty.", str
        )
        semester = prompt_new_value(
            "Semester", current_semester, validate_semester,
            "Semester must be between 1 and 8.", int
        )
        phone = prompt_new_value(
            "Phone", current_phone, validate_phone,
            "Phone number must contain exactly 10 digits.", str
        )
        email = prompt_new_value(
            "Email", current_email, validate_email,
            "Please enter a valid email address.", str
        )
        address = prompt_new_value(
            "Address", current_address, validate_name,
            "Address cannot be empty.", str
        )
        photo_path = prompt_new_value(
            "Photo Path", current_photo_path, lambda v: True,
            "", str
        )
        admission_date = prompt_new_value(
            "Admission Date (YYYY-MM-DD)", current_admission_date,
            validate_date_format,
            "Date must be a valid YYYY-MM-DD date, not in the future.", str
        )

        # ---- Update the record using a parameterized query ----
        update_query = """
            UPDATE students
            SET name = ?, dob = ?, age = ?, gender = ?, department = ?,
                semester = ?, phone = ?, email = ?, address = ?,
                photo_path = ?, admission_date = ?
            WHERE id = ?
        """

        cursor.execute(
            update_query,
            (name, dob, age, gender, department, semester, phone,
             email, address, photo_path, admission_date, student_id)
        )
        connection.commit()
        print_success(f"\n[SUCCESS] Student ID {student_id} updated successfully.\n")

    except sqlite3.Error as error:
        print_error(f"\n[ERROR] Update failed: {error}\n")
    finally:
        connection.close()
