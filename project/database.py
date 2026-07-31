"""
database.py
------------
This module is responsible for all database-level setup for the
Student Management System.

It contains:
    - A function to create/get a connection to the SQLite database.
    - A function to create the 'students' table if it does not exist.
    - A function to create the 'admins' table (used for login) and
      seed it with a default admin account on first run.

Keeping database connection logic in a single module makes the code
modular and easy to maintain (Single Responsibility Principle).
"""

import sqlite3
import os
import hashlib

# Name of the SQLite database file.
# It will be created automatically in the same folder as this script.
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")

# Default admin credentials created automatically on first run.
# The user should change this password after logging in for the
# first time (see README.md for how).
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"


def get_connection():
    """
    Create and return a new SQLite database connection.

    Using a fresh connection per operation (instead of one global
    connection) is a simple and safe approach for small CLI apps
    like this one — it avoids issues with the connection being
    left open or shared incorrectly between functions.

    Returns:
        sqlite3.Connection: An active connection object to students.db
    """
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_students_table(cursor):
    """
    Create the 'students' table if it does not already exist.

    Table Schema:
        id              -> INTEGER, Primary Key, Auto Increment
        name            -> TEXT, Student's full name
        dob             -> TEXT, Date of Birth (YYYY-MM-DD)
        age             -> INTEGER, Student's age
        gender          -> TEXT, Student's gender
        department      -> TEXT, Department/branch of study
        semester        -> INTEGER, Current semester (1-8)
        phone           -> TEXT, 10-digit phone number
        email           -> TEXT, Valid email address
        address         -> TEXT, Residential address
        photo_path      -> TEXT, File path to the student's photo (optional)
        admission_date  -> TEXT, Date the student was admitted (YYYY-MM-DD)
    """
    create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dob TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            photo_path TEXT,
            admission_date TEXT NOT NULL
        );
    """
    cursor.execute(create_table_query)


def create_admins_table(cursor):
    """
    Create the 'admins' table used for the login system, and seed it
    with one default admin account if the table is empty.

    Passwords are never stored in plain text — they are hashed with
    SHA-256 before being saved.
    """
    create_table_query = """
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
    """
    cursor.execute(create_table_query)

    # Seed a default admin account only if no admins exist yet.
    cursor.execute("SELECT COUNT(*) FROM admins")
    admin_count = cursor.fetchone()[0]

    if admin_count == 0:
        hashed_password = hashlib.sha256(
            DEFAULT_ADMIN_PASSWORD.encode("utf-8")
        ).hexdigest()
        cursor.execute(
            "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
            (DEFAULT_ADMIN_USERNAME, hashed_password),
        )


def initialize_database():
    """
    Public entry point to set up the database.
    Called from main.py at program startup.

    Creates both the 'students' and 'admins' tables if they don't
    already exist, and seeds a default admin account.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        create_students_table(cursor)
        create_admins_table(cursor)
        connection.commit()
        print(f"[INFO] Database ready at: {DB_NAME}")
    except sqlite3.Error as error:
        print(f"[ERROR] Could not initialize database: {error}")
    finally:
        connection.close()
