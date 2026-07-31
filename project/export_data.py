"""
export_data.py
---------------
This module handles exporting all student records to a CSV file.

The exported file can be opened directly in Excel, Google Sheets,
or any spreadsheet application — useful for reports, backups, or
sharing data with people who don't use this program.
"""

import csv
import sqlite3
import os
from datetime import datetime
from database import get_connection
from colors import print_success, print_error, print_info, print_header

# Column headers matching the 'students' table structure.
CSV_HEADERS = [
    "ID", "Name", "Date of Birth", "Age", "Gender", "Department",
    "Semester", "Phone", "Email", "Address", "Photo Path",
    "Admission Date"
]


def export_to_csv():
    """
    Export all student records from the database to a timestamped
    CSV file in the project folder (e.g., students_export_20260712_143000.csv).
    """
    print_header("\n----- EXPORT TO CSV -----")

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students ORDER BY id ASC")
        students = cursor.fetchall()

        if not students:
            print_info("\n[INFO] No student records to export.\n")
            return

        # Build a unique filename using the current date/time so
        # repeated exports don't overwrite each other.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_folder = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(project_folder, f"students_export_{timestamp}.csv")

        with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(CSV_HEADERS)
            writer.writerows(students)

        print_success(f"\n[SUCCESS] Exported {len(students)} record(s) to:")
        print_success(f"          {filename}\n")

    except (sqlite3.Error, OSError) as error:
        print_error(f"\n[ERROR] Export failed: {error}\n")
    finally:
        connection.close()
