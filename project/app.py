"""
app.py
------
Flask entry point for the Student Management System web application.

This file coexists with the console app (main.py). It reuses ALL
existing business logic instead of rewriting it:

    - database.py    -> get_connection(), initialize_database()
    - auth.py         -> hash_password(), verify_credentials()
    - utils.py         -> every validate_* function + calculate_age_from_dob()

No console-only modules (banner.py, colors.py) are needed here since
this is a browser-based UI, but nothing in those files is touched.
"""

import csv
import io
import os
import sqlite3
from datetime import datetime, date
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, send_file, jsonify
)
from werkzeug.utils import secure_filename

from database import get_connection, initialize_database
from auth import hash_password, verify_credentials
from utils import (
    validate_name, validate_age, validate_phone, validate_email,
    validate_semester, validate_gender, validate_date_format,
    calculate_age_from_dob,
)

app = Flask(__name__)

# Secret key is required by Flask for session management.
# A real deployment should load this from an environment variable.
app.config["SECRET_KEY"] = os.environ.get(
    "SMS_SECRET_KEY", "dev-secret-key-change-this-in-production"
)

# Where uploaded student photos are stored (served as static files).
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "static", "uploads"
)
ALLOWED_PHOTO_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_PHOTO_SIZE_BYTES = 3 * 1024 * 1024  # 3 MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_PHOTO_SIZE_BYTES
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

STUDENT_COLUMNS = [
    "id", "name", "dob", "age", "gender", "department", "semester",
    "phone", "email", "address", "photo_path", "admission_date",
]

PER_PAGE = 10


# ---------------------------------------------------------------- #
# Helpers
# ---------------------------------------------------------------- #

def row_to_dict(row):
    """Convert a sqlite3 student row tuple into a labelled dict."""
    return dict(zip(STUDENT_COLUMNS, row)) if row else None


def allowed_photo(filename):
    """Check the uploaded file has an allowed image extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_PHOTO_EXTENSIONS
    )


def save_photo(file_storage, student_id):
    """
    Securely save an uploaded photo and return its relative static
    path, or None if no valid file was supplied.
    """
    if not file_storage or file_storage.filename == "":
        return None
    if not allowed_photo(file_storage.filename):
        flash("Photo must be a PNG, JPG, JPEG, GIF, or WEBP file.", "warning")
        return None

    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(
        f"student_{student_id}_{int(datetime.now().timestamp())}.{ext}"
    )
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file_storage.save(file_path)
    return f"uploads/{filename}"


def login_required(view_func):
    """Redirect anonymous visitors to the login page."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("username"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login", next=request.path))
        return view_func(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_globals():
    """Make the logged-in username and dark-mode flag available to
    every template without passing them explicitly each time."""
    return {
        "current_user": session.get("username"),
        "dark_mode": session.get("dark_mode", False),
        "current_year": date.today().year,
    }


# ---------------------------------------------------------------- #
# Auth routes  (Phase 1)
# ---------------------------------------------------------------- #

@app.route("/")
def home():
    if session.get("username"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        remember = request.form.get("remember") == "on"

        if verify_credentials(username, password):
            session["username"] = username
            session.permanent = remember  # "Remember me" -> longer-lived cookie
            flash(f"Welcome back, {username}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ---------------------------------------------------------------- #
# Dashboard  (Phase 2)
# ---------------------------------------------------------------- #

@app.route("/dashboard")
@login_required
def dashboard():
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students WHERE gender = 'Male'")
        male_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students WHERE gender = 'Female'")
        female_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT department) FROM students")
        department_count = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(age) FROM students")
        avg_age = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT department, COUNT(*) FROM students "
            "GROUP BY department ORDER BY COUNT(*) DESC"
        )
        department_rows = cursor.fetchall()

        cursor.execute(
            "SELECT gender, COUNT(*) FROM students GROUP BY gender"
        )
        gender_rows = cursor.fetchall()

        cursor.execute(
            "SELECT semester, COUNT(*) FROM students "
            "GROUP BY semester ORDER BY semester"
        )
        semester_rows = cursor.fetchall()

        cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 5")
        recent_students = [row_to_dict(r) for r in cursor.fetchall()]

    except sqlite3.Error as error:
        flash(f"Could not load dashboard data: {error}", "danger")
        total_students = male_count = female_count = department_count = 0
        avg_age = 0
        department_rows = gender_rows = semester_rows = []
        recent_students = []
    finally:
        connection.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        male_count=male_count,
        female_count=female_count,
        department_count=department_count,
        avg_age=round(avg_age, 1),
        department_labels=[r[0] for r in department_rows],
        department_data=[r[1] for r in department_rows],
        gender_labels=[r[0] for r in gender_rows],
        gender_data=[r[1] for r in gender_rows],
        semester_labels=[str(r[0]) for r in semester_rows],
        semester_data=[r[1] for r in semester_rows],
        recent_students=recent_students,
    )


# ---------------------------------------------------------------- #
# Student management  (Phase 3 & 4 - list/search/filter/sort/paginate)
# ---------------------------------------------------------------- #

@app.route("/students")
@login_required
def students_list():
    search = request.args.get("q", "").strip()
    department = request.args.get("department", "").strip()
    semester = request.args.get("semester", "").strip()
    gender = request.args.get("gender", "").strip()
    search_by = request.args.get("search_by", "name")  # name | id | email
    sort_by = request.args.get("sort_by", "id")
    sort_dir = request.args.get("sort_dir", "asc")
    page = max(1, request.args.get("page", 1, type=int))

    allowed_sort_columns = {
        "id", "name", "age", "department", "semester", "admission_date"
    }
    if sort_by not in allowed_sort_columns:
        sort_by = "id"
    sort_dir = "DESC" if sort_dir.lower() == "desc" else "ASC"

    conditions = []
    params = []

    if search:
        if search_by == "id" and search.isdigit():
            conditions.append("id = ?")
            params.append(int(search))
        elif search_by == "email":
            conditions.append("email LIKE ?")
            params.append(f"%{search}%")
        else:
            conditions.append("name LIKE ?")
            params.append(f"%{search}%")

    if department:
        conditions.append("department = ?")
        params.append(department)
    if semester:
        conditions.append("semester = ?")
        params.append(semester)
    if gender:
        conditions.append("gender = ?")
        params.append(gender)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM students {where_clause}", params)
        total_count = cursor.fetchone()[0]
        total_pages = max(1, (total_count + PER_PAGE - 1) // PER_PAGE)
        page = min(page, total_pages)
        offset = (page - 1) * PER_PAGE

        query = (
            f"SELECT * FROM students {where_clause} "
            f"ORDER BY {sort_by} {sort_dir} LIMIT ? OFFSET ?"
        )
        cursor.execute(query, params + [PER_PAGE, offset])
        students = [row_to_dict(r) for r in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT department FROM students ORDER BY department")
        departments = [r[0] for r in cursor.fetchall()]

    except sqlite3.Error as error:
        flash(f"Search failed: {error}", "danger")
        students, departments = [], []
        total_count, total_pages = 0, 1
    finally:
        connection.close()

    return render_template(
        "students_list.html",
        students=students,
        departments=departments,
        total_count=total_count,
        total_pages=total_pages,
        page=page,
        search=search,
        department=department,
        semester=semester,
        gender=gender,
        search_by=search_by,
        sort_by=sort_by,
        sort_dir=sort_dir.lower(),
    )


@app.route("/students/search-live")
@login_required
def students_search_live():
    """JSON endpoint powering the live-search typeahead."""
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, department, email FROM students "
            "WHERE name LIKE ? OR email LIKE ? LIMIT 8",
            (f"%{q}%", f"%{q}%"),
        )
        results = [
            {"id": r[0], "name": r[1], "department": r[2], "email": r[3]}
            for r in cursor.fetchall()
        ]
    except sqlite3.Error:
        results = []
    finally:
        connection.close()

    return jsonify(results)


def _collect_and_validate_student_form():
    """
    Shared validation for the add/edit student form. Reuses the exact
    same validator functions as the console app. Returns
    (data_dict, errors_list).
    """
    form = request.form
    errors = []

    name = form.get("name", "").strip()
    if not validate_name(name):
        errors.append("Name cannot be empty.")

    dob = form.get("dob", "").strip()
    age = None
    if not validate_date_format(dob):
        errors.append("Date of Birth must be a valid date, not in the future.")
    else:
        age = calculate_age_from_dob(dob)
        if not validate_age(age):
            errors.append(
                f"Calculated age is {age}, but age must be between 16 and 35."
            )

    gender = form.get("gender", "").strip()
    if not validate_gender(gender):
        errors.append("Gender must be Male, Female, or Other.")
    gender = gender.capitalize()

    department = form.get("department", "").strip()
    if not validate_name(department):
        errors.append("Department cannot be empty.")

    semester_raw = form.get("semester", "").strip()
    semester = None
    if not semester_raw.isdigit() or not validate_semester(int(semester_raw)):
        errors.append("Semester must be a whole number between 1 and 8.")
    else:
        semester = int(semester_raw)

    phone = form.get("phone", "").strip()
    if not validate_phone(phone):
        errors.append("Phone number must contain exactly 10 digits.")

    email = form.get("email", "").strip()
    if not validate_email(email):
        errors.append("Please enter a valid email address.")

    address = form.get("address", "").strip()
    if not validate_name(address):
        errors.append("Address cannot be empty.")

    admission_date = form.get("admission_date", "").strip() or date.today().isoformat()
    if not validate_date_format(admission_date):
        errors.append("Admission Date must be a valid date, not in the future.")

    data = {
        "name": name, "dob": dob, "age": age, "gender": gender,
        "department": department, "semester": semester, "phone": phone,
        "email": email, "address": address, "admission_date": admission_date,
    }
    return data, errors


@app.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student_route():
    if request.method == "POST":
        data, errors = _collect_and_validate_student_form()

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("student_form.html", mode="add", form=request.form)

        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO students
                   (name, dob, age, gender, department, semester, phone,
                    email, address, photo_path, admission_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (data["name"], data["dob"], data["age"], data["gender"],
                 data["department"], data["semester"], data["phone"],
                 data["email"], data["address"], "N/A", data["admission_date"])
            )
            new_id = cursor.lastrowid

            photo_file = request.files.get("photo")
            photo_path = save_photo(photo_file, new_id)
            if photo_path:
                cursor.execute(
                    "UPDATE students SET photo_path = ? WHERE id = ?",
                    (photo_path, new_id)
                )

            connection.commit()
            flash(f"Student '{data['name']}' added successfully (ID {new_id}).", "success")
            return redirect(url_for("student_profile", student_id=new_id))
        except sqlite3.Error as error:
            flash(f"Failed to add student: {error}", "danger")
            return render_template("student_form.html", mode="add", form=request.form)
        finally:
            connection.close()

    return render_template("student_form.html", mode="add", form={})


@app.route("/students/<int:student_id>")
@login_required
def student_profile(student_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = row_to_dict(cursor.fetchone())
    except sqlite3.Error as error:
        flash(f"Could not load student: {error}", "danger")
        student = None
    finally:
        connection.close()

    if not student:
        flash("Student not found.", "warning")
        return redirect(url_for("students_list"))

    return render_template("student_profile.html", student=student)


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student_route(student_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        current = row_to_dict(cursor.fetchone())

        if not current:
            flash("Student not found.", "warning")
            return redirect(url_for("students_list"))

        if request.method == "POST":
            data, errors = _collect_and_validate_student_form()

            if errors:
                for e in errors:
                    flash(e, "danger")
                merged = {**current, **request.form}
                return render_template("student_form.html", mode="edit",
                                        form=merged, student=current)

            photo_path = current["photo_path"]
            photo_file = request.files.get("photo")
            new_photo_path = save_photo(photo_file, student_id)
            if new_photo_path:
                photo_path = new_photo_path

            cursor.execute(
                """UPDATE students
                   SET name=?, dob=?, age=?, gender=?, department=?,
                       semester=?, phone=?, email=?, address=?,
                       photo_path=?, admission_date=?
                   WHERE id=?""",
                (data["name"], data["dob"], data["age"], data["gender"],
                 data["department"], data["semester"], data["phone"],
                 data["email"], data["address"], photo_path,
                 data["admission_date"], student_id)
            )
            connection.commit()
            flash(f"Student ID {student_id} updated successfully.", "success")
            return redirect(url_for("student_profile", student_id=student_id))

    except sqlite3.Error as error:
        flash(f"Update failed: {error}", "danger")
        return redirect(url_for("students_list"))
    finally:
        connection.close()

    return render_template("student_form.html", mode="edit", form=current, student=current)


@app.route("/students/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_student_route(student_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        if not row:
            flash("Student not found.", "warning")
            return redirect(url_for("students_list"))

        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        flash(f"Student '{row[0]}' (ID {student_id}) was deleted.", "success")
    except sqlite3.Error as error:
        flash(f"Deletion failed: {error}", "danger")
    finally:
        connection.close()

    return redirect(url_for("students_list"))


# ---------------------------------------------------------------- #
# Reports  (Phase 5)
# ---------------------------------------------------------------- #

@app.route("/reports")
@login_required
def reports():
    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(age) FROM students")
        avg_age = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT department, COUNT(*) FROM students "
            "GROUP BY department ORDER BY COUNT(*) DESC"
        )
        by_department = cursor.fetchall()

        cursor.execute("SELECT gender, COUNT(*) FROM students GROUP BY gender")
        by_gender = cursor.fetchall()

        cursor.execute(
            "SELECT semester, COUNT(*) FROM students "
            "GROUP BY semester ORDER BY semester"
        )
        by_semester = cursor.fetchall()

        cursor.execute(
            "SELECT * FROM students ORDER BY admission_date DESC LIMIT 10"
        )
        recent_admissions = [row_to_dict(r) for r in cursor.fetchall()]

    except sqlite3.Error as error:
        flash(f"Could not load reports: {error}", "danger")
        total, avg_age = 0, 0
        by_department = by_gender = by_semester = []
        recent_admissions = []
    finally:
        connection.close()

    return render_template(
        "reports.html",
        total=total,
        avg_age=round(avg_age, 1),
        by_department=by_department,
        by_gender=by_gender,
        by_semester=by_semester,
        recent_admissions=recent_admissions,
    )


# ---------------------------------------------------------------- #
# Export  (Phase 6) - reuses the same column layout as export_data.py
# ---------------------------------------------------------------- #

@app.route("/export/csv")
@login_required
def export_csv_route():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students ORDER BY id ASC")
        students = cursor.fetchall()
    except sqlite3.Error as error:
        flash(f"Export failed: {error}", "danger")
        return redirect(url_for("reports"))
    finally:
        connection.close()

    if not students:
        flash("No student records to export.", "info")
        return redirect(url_for("reports"))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Name", "Date of Birth", "Age", "Gender", "Department",
        "Semester", "Phone", "Email", "Address", "Photo Path",
        "Admission Date"
    ])
    writer.writerows(students)

    mem_file = io.BytesIO(output.getvalue().encode("utf-8"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(
        mem_file,
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"students_export_{timestamp}.csv",
    )


# ---------------------------------------------------------------- #
# Settings  (Phase 7)
# ---------------------------------------------------------------- #

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "change_password":
            current_password = request.form.get("current_password", "").strip()
            new_password = request.form.get("new_password", "").strip()
            confirm_password = request.form.get("confirm_password", "").strip()

            if not verify_credentials(session["username"], current_password):
                flash("Current password is incorrect.", "danger")
            elif not new_password:
                flash("New password cannot be empty.", "warning")
            elif new_password != confirm_password:
                flash("New passwords do not match.", "danger")
            else:
                connection = get_connection()
                try:
                    cursor = connection.cursor()
                    cursor.execute(
                        "UPDATE admins SET password_hash = ? WHERE username = ?",
                        (hash_password(new_password), session["username"])
                    )
                    connection.commit()
                    flash("Password updated successfully.", "success")
                except sqlite3.Error as error:
                    flash(f"Could not update password: {error}", "danger")
                finally:
                    connection.close()

        elif form_type == "toggle_dark_mode":
            session["dark_mode"] = not session.get("dark_mode", False)

        return redirect(url_for("settings"))

    connection = get_connection()
    try:
        db_path = connection.execute("PRAGMA database_list").fetchone()[2]
        total_students = connection.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]
    finally:
        connection.close()

    db_size_kb = round(os.path.getsize(db_path) / 1024, 1) if os.path.exists(db_path) else 0

    return render_template(
        "settings.html",
        db_size_kb=db_size_kb,
        total_students=total_students,
    )


@app.route("/settings/backup")
@login_required
def backup_database():
    """Download a timestamped copy of the live SQLite database file."""
    connection = get_connection()
    db_path = connection.execute("PRAGMA database_list").fetchone()[2]
    connection.close()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(
        db_path,
        as_attachment=True,
        download_name=f"students_backup_{timestamp}.db",
    )


# ---------------------------------------------------------------- #
# Error handlers  (Phase 8/9)
# ---------------------------------------------------------------- #

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


@app.errorhandler(413)
def file_too_large(error):
    flash("Uploaded file is too large (max 3 MB).", "danger")
    return redirect(request.referrer or url_for("dashboard"))


if __name__ == "__main__":
    # Make sure the database and tables exist (reuses the exact
    # same function the console app calls at startup).
    initialize_database()

    # debug=True enables auto-reload and detailed error pages during
    # development. This should be turned off in production.
    app.run(debug=True)
