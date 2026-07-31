"""
utils.py
--------
This module contains reusable helper/utility functions used across
the Student Management System, such as:

    - Input validation (name, age, phone, email, semester, gender,
      date of birth, admission date)
    - Formatted, colored table printing for displaying student records
    - Generic validated-input prompts

Keeping validation logic here avoids code duplication across
add_student.py and update_student.py.
"""

import re
from datetime import datetime, date
from colors import Fore, Style, print_info

# Regular expression pattern for validating email addresses.
# Matches: someone@example.com, first.last@sub.domain.co.in, etc.
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Expected format for all date fields in this project.
DATE_FORMAT = "%Y-%m-%d"


def validate_name(name):
    """Validate that a name (or department) is not empty/whitespace."""
    return bool(name and name.strip())


def validate_age(age):
    """Validate that age is an integer between 16 and 35 (inclusive)."""
    return 16 <= age <= 35


def validate_phone(phone):
    """Validate that the phone number contains exactly 10 digits."""
    return bool(re.fullmatch(r"\d{10}", phone))


def validate_email(email):
    """Validate the email address format using a regular expression."""
    return bool(re.fullmatch(EMAIL_PATTERN, email))


def validate_semester(semester):
    """Validate that the semester is between 1 and 8 (inclusive)."""
    return 1 <= semester <= 8


def validate_gender(gender):
    """Validate that gender is one of the accepted values."""
    return gender.strip().capitalize() in ("Male", "Female", "Other")


def validate_date_format(date_string):
    """
    Validate that a string is a real calendar date in YYYY-MM-DD format
    and is not set in the future.

    Args:
        date_string (str): The date entered by the user.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        parsed_date = datetime.strptime(date_string, DATE_FORMAT).date()
        return parsed_date <= date.today()
    except ValueError:
        return False


def validate_photo_path(photo_path):
    """
    Validate the (optional) photo path field.
    An empty string is allowed (photo is optional) — it will be
    stored as 'N/A'. Otherwise, any non-empty text is accepted,
    since the file may live on a different machine than the one
    running this validation.

    Args:
        photo_path (str): The path entered by the user.

    Returns:
        bool: Always True (field is optional / free-text).
    """
    return True


def calculate_age_from_dob(dob_string):
    """
    Calculate age in whole years from a date of birth string.

    Args:
        dob_string (str): Date of birth in YYYY-MM-DD format.

    Returns:
        int: Age in years.
    """
    dob = datetime.strptime(dob_string, DATE_FORMAT).date()
    today = date.today()
    years = today.year - dob.year
    # Adjust if birthday hasn't occurred yet this year.
    if (today.month, today.day) < (dob.month, dob.day):
        years -= 1
    return years


def get_valid_int(prompt, validator, error_message):
    """
    Repeatedly prompt the user until a valid integer is entered
    that satisfies the given validator function.
    """
    while True:
        try:
            value = int(input(prompt))
            if validator(value):
                return value
            print(f"{Fore.RED}[INVALID] {error_message}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}[INVALID] Please enter a valid whole number."
                  f"{Style.RESET_ALL}")


def get_valid_str(prompt, validator, error_message):
    """
    Repeatedly prompt the user until a valid string is entered
    that satisfies the given validator function.
    """
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f"{Fore.RED}[INVALID] {error_message}{Style.RESET_ALL}")


def get_valid_date(prompt, allow_blank_for_today=False):
    """
    Repeatedly prompt the user for a date in YYYY-MM-DD format.

    Args:
        prompt (str): The message shown to the user.
        allow_blank_for_today (bool): If True, pressing Enter with no
            input will default to today's date (used for admission date).

    Returns:
        str: A validated date string in YYYY-MM-DD format.
    """
    while True:
        value = input(prompt).strip()

        if allow_blank_for_today and value == "":
            return date.today().strftime(DATE_FORMAT)

        if validate_date_format(value):
            return value

        print(f"{Fore.RED}[INVALID] Please enter a valid date in "
              f"YYYY-MM-DD format (not in the future).{Style.RESET_ALL}")


def print_student_table(students):
    """
    Print a list of student records in a clean, aligned tabular format.
    Shows the core fields; use print_single_student() for full details
    (including DOB, address, photo path, and admission date).

    Args:
        students (list of tuples): Each tuple represents one row:
            (id, name, dob, age, gender, department, semester,
             phone, email, address, photo_path, admission_date)
    """
    if not students:
        print_info("\n[INFO] No student records found.\n")
        return

    headers = ["ID", "Name", "Age", "Gender", "Department",
               "Semester", "Phone", "Email"]

    row_format = "{:<5} {:<20} {:<5} {:<8} {:<15} {:<9} {:<12} {:<25}"

    print(f"\n{Fore.CYAN}{'=' * 105}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}"
          f"{row_format.format(*headers)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 105}{Style.RESET_ALL}")

    for student in students:
        (student_id, name, dob, age, gender, department, semester,
         phone, email, address, photo_path, admission_date) = student
        print(row_format.format(
            student_id, name, age, gender, department,
            semester, phone, email
        ))

    print(f"{Fore.CYAN}{'=' * 105}{Style.RESET_ALL}")
    print_info(f"Total Records: {len(students)}\n"
               f"(Tip: use Search to see full details including DOB, "
               f"address, photo path, and admission date.)\n")


def print_single_student(student):
    """
    Print the full details of a single student in a readable format,
    including the newer fields (DOB, address, photo path, admission date).

    Args:
        student (tuple): (id, name, dob, age, gender, department,
                           semester, phone, email, address,
                           photo_path, admission_date)
    """
    if not student:
        print(f"{Fore.RED}\n[NOT FOUND] Student Not Found.\n{Style.RESET_ALL}")
        return

    (student_id, name, dob, age, gender, department, semester,
     phone, email, address, photo_path, admission_date) = student

    print(f"\n{Fore.YELLOW}{'-' * 45}{Style.RESET_ALL}")
    print(f"Student ID     : {student_id}")
    print(f"Name           : {name}")
    print(f"Date of Birth  : {dob}")
    print(f"Age            : {age}")
    print(f"Gender         : {gender}")
    print(f"Department     : {department}")
    print(f"Semester       : {semester}")
    print(f"Phone          : {phone}")
    print(f"Email          : {email}")
    print(f"Address        : {address}")
    print(f"Photo Path     : {photo_path if photo_path else 'N/A'}")
    print(f"Admission Date : {admission_date}")
    print(f"{Fore.YELLOW}{'-' * 45}{Style.RESET_ALL}\n")
