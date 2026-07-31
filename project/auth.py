"""
auth.py
-------
Handles the admin login system for the Student Management System.

Passwords are stored as SHA-256 hashes in the 'admins' table
(never in plain text). This module provides:

    - login_screen(): prompts for username/password, allows a
      limited number of attempts.
    - change_password(): lets a logged-in admin change their password.

NOTE: SHA-256 hashing is used here for simplicity and to keep the
project free of third-party dependencies. In a real production
system you would use a slower, salted hashing scheme such as
bcrypt or Argon2, which are designed specifically for passwords.
"""

import hashlib
import sqlite3
from database import get_connection
from colors import print_success, print_error, print_warning, print_title

MAX_LOGIN_ATTEMPTS = 3


def hash_password(password):
    """
    Hash a plain-text password using SHA-256.

    Args:
        password (str): The plain-text password.

    Returns:
        str: The hexadecimal hash of the password.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_credentials(username, password):
    """
    Check whether the given username/password combination is valid.

    Args:
        username (str): The entered username.
        password (str): The entered plain-text password.

    Returns:
        bool: True if credentials are correct, False otherwise.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT password_hash FROM admins WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()

        if row is None:
            return False

        stored_hash = row[0]
        return stored_hash == hash_password(password)
    except sqlite3.Error as error:
        print_error(f"[ERROR] Login check failed: {error}")
        return False
    finally:
        connection.close()


def login_screen():
    """
    Display the login screen and prompt for credentials.
    Allows up to MAX_LOGIN_ATTEMPTS attempts before exiting.

    Returns:
        str or None: The logged-in username if successful, else None.
    """
    print_title("\n==============================")
    print_title("   STUDENT MANAGEMENT SYSTEM")
    print_title("         ADMIN LOGIN")
    print_title("==============================")

    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if verify_credentials(username, password):
            print_success(f"\n[SUCCESS] Welcome, {username}!\n")
            return username

        remaining = MAX_LOGIN_ATTEMPTS - attempt
        if remaining > 0:
            print_error(
                f"[FAILED] Incorrect username or password. "
                f"{remaining} attempt(s) remaining.\n"
            )
        else:
            print_error("\n[FAILED] Too many failed attempts. Exiting.\n")

    return None


def change_password(current_username):
    """
    Allow the currently logged-in admin to change their password.

    Args:
        current_username (str): The username of the logged-in admin.
    """
    print("\n----- CHANGE PASSWORD -----")
    current_password = input("Enter current password: ").strip()

    if not verify_credentials(current_username, current_password):
        print_error("\n[FAILED] Current password is incorrect.\n")
        return

    new_password = input("Enter new password: ").strip()
    confirm_password = input("Confirm new password: ").strip()

    if not new_password:
        print_warning("\n[CANCELLED] Password cannot be empty.\n")
        return

    if new_password != confirm_password:
        print_error("\n[FAILED] Passwords do not match.\n")
        return

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE admins SET password_hash = ? WHERE username = ?",
            (hash_password(new_password), current_username)
        )
        connection.commit()
        print_success("\n[SUCCESS] Password updated successfully.\n")
    except sqlite3.Error as error:
        print_error(f"\n[ERROR] Could not update password: {error}\n")
    finally:
        connection.close()
