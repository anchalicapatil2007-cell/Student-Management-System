# 🎓 Student Management System

A **Student Management System** built with **Python 3**, **Flask**, and
**SQLite**, available in two editions that share the exact same
database and business logic:

1. **Console Edition** (`main.py`) — the original menu-driven CLI app.
2. **Web Edition** (`app.py`) — a full Bootstrap 5 admin dashboard /
   College ERP web app: login, dashboard with Chart.js charts, full
   student CRUD with photo upload, live search & filters, reports,
   CSV export, dark mode, and settings.

Both editions read and write the same `students.db` SQLite file, and
both reuse the same validation (`utils.py`), authentication (`auth.py`),
and database (`database.py`) modules — no logic is duplicated.

Designed as a clean, modular, and professional mini-project — ideal for
a second-year AI & Data Science (AIDS) engineering student to learn
database integration, authentication, input validation, and full-stack
web development.

---

## 🌐 Web Edition (Flask)

### Running the web app

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** and log in with the same default
credentials as the console app (`admin` / `admin123`).

### Web Edition Features

| Area | What you get |
|---|---|
| 🔐 Login | Bootstrap 5 glassmorphism login card, gradient background, remember-me, invalid-login alerts, session-based auth reusing `auth.py` |
| 📊 Dashboard | Responsive sidebar + navbar, stat cards (total/male/female/departments/avg age), Chart.js gender/department/semester charts, recent students, quick actions |
| 👥 Students | Full CRUD, profile pages, photo upload with preview, Bootstrap sortable/paginated table |
| 🔎 Search | Live-search typeahead, filters by department/semester/gender, search by name/ID/email |
| 📈 Reports | Department/gender/semester statistics with charts, recent admissions |
| 📁 Export | One-click CSV download (same column layout as the console export) |
| ⚙️ Settings | Change password, dark mode toggle, database backup download, system info |
| 🎨 UI polish | Toast notifications, delete confirmation dialogs, loading spinner, breadcrumbs, custom 404/500 pages, fully responsive/mobile-friendly |

### Web Edition File/Folder Additions

```
app.py                  # Flask app — all routes (auth, dashboard, CRUD, reports, export, settings)
templates/               # Jinja2 templates (base, login, dashboard, students, forms, reports, settings, errors)
static/css/style.css      # Design tokens, gradient/glassmorphism, sidebar, dark mode, responsive layout
static/js/main.js          # Sidebar toggle, toasts, delete confirmations, live search, photo preview
static/uploads/              # Uploaded student photos (created automatically)
```

`app.py` imports directly from `database.py`, `auth.py`, and
`utils.py` — the same modules the console app uses — so any future fix
to validation or auth logic automatically applies to both editions.

---

## 🖥️ Console Edition

---

## 📌 Project Description

The Student Management System allows an administrator (e.g., a college
office or teacher) to manage student records through a secure,
menu-driven command-line interface. All data is stored persistently in
a local SQLite database (`students.db`), which is created automatically
the first time the program runs — along with a default admin account.

The project demonstrates good software engineering practices such as:

- Modular code organization (one responsibility per file)
- Password-protected access (SHA-256 hashed credentials)
- Input validation using regular expressions and date parsing
- Parameterized SQL queries (protection against SQL injection)
- Exception handling with `try-except`
- Colored, readable terminal output
- PEP 8 compliant, well-commented code

---

## ✨ Features

| # | Feature              | Description                                                          |
|---|------------------------|------------------------------------------------------------------------|
| 1 | 🔐 Admin Login         | Password-protected access with hashed credentials (3 attempt limit) |
| 2 | Add Student            | Add a new student with full input validation                        |
| 3 | View All Students      | Display all records in a neatly formatted, colored table            |
| 4 | Search Student          | Search by Student ID (exact) or Name (partial, case-insensitive)   |
| 5 | Update Student          | Edit any field of an existing student, keeping unchanged fields    |
| 6 | Delete Student          | Delete a student after a confirmation prompt                        |
| 7 | Count Students          | Show the total number of students in the database                   |
| 8 | 📊 Dashboard            | Visual summary — totals, average age, breakdowns by department/gender/semester |
| 9 | 📁 Export to CSV        | Export all records to a timestamped `.csv` file (opens in Excel)   |
| 10| 🔑 Change Password      | Let the logged-in admin change their password securely             |
| 11| 🎨 Colored Output       | Green (success), red (error), yellow (warning), cyan (info)        |

### New Student Fields

- 📸 **Photo Path** — file path reference to the student's photo (optional)
- 🎂 **Date of Birth** — used to automatically calculate and validate Age
- 🏠 **Address** — residential address
- 📅 **Admission Date** — defaults to today if left blank

### Validation Rules

- **Name** — cannot be empty
- **Date of Birth** — must be a real calendar date (`YYYY-MM-DD`), not in the future
- **Age** — automatically calculated from DOB; must fall between 16 and 35
- **Gender** — must be Male, Female, or Other
- **Phone** — must contain exactly 10 digits
- **Email** — validated using a regular expression
- **Semester** — must be between 1 and 8
- **Admission Date** — must be a real date, not in the future

---

## 📁 Folder Structure

```
Student_Management_System/
│
├── main.py              # Entry point — login, menu, and routing
├── database.py          # Database connection, table creation, default admin seed
├── auth.py               # Login system (hashing, verification, password change)
├── colors.py              # Centralized colored-terminal-output helpers
├── add_student.py         # Add new student (with validation)
├── view_student.py        # View all students / count students
├── search_student.py      # Search by ID or Name
├── update_student.py      # Update existing student details
├── delete_student.py      # Delete a student (with confirmation)
├── dashboard.py            # Statistics dashboard (totals, breakdowns, charts)
├── export_data.py          # Export all records to CSV
├── utils.py                 # Shared validation & display helper functions
├── requirements.txt          # Python dependencies (colorama)
├── students.db                # SQLite database (auto-created on first run)
├── students_export_*.csv       # Generated when you use "Export to CSV"
└── README.md                    # Project documentation
```

---

## 🛠 Technologies Used

- **Language:** Python 3
- **Database:** SQLite (via Python's built-in `sqlite3` module)
- **IDE:** Visual Studio Code
- **Standard Library Modules:** `sqlite3`, `re`, `os`, `csv`, `hashlib`, `datetime`
- **Third-Party Package:** [`colorama`](https://pypi.org/project/colorama/) — for cross-platform colored terminal text

---

## ⚙️ How to Install

1. **Install Python 3** (3.8 or higher recommended)
   ```bash
   python --version
   ```

2. **Download/Clone the project** into a folder:
   ```bash
   git clone <your-repo-url>
   cd Student_Management_System
   ```

3. **Install dependencies** (just `colorama`, for colored output):
   ```bash
   pip install -r requirements.txt
   ```
   > If you skip this step, the program still runs perfectly fine —
   > it will just print plain, uncolored text instead.

---

## ▶️ How to Run (in VS Code)

1. Open the `Student_Management_System` folder in **VS Code**
   (`File → Open Folder...`).
2. Open the integrated terminal (`Ctrl + ~`).
3. Install dependencies (first time only):
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. On first run, the database and a **default admin account** are
   created automatically:
   ```
   [INFO] Database ready at: .../students.db
   ```
6. **Log in** using the default credentials:
   ```
   Username: admin
   Password: admin123
   ```
   ⚠️ **Change this password immediately** using menu option **9**
   after your first login — see [Login & Security](#-login--security) below.
7. Use the menu to add, view, search, update, delete, or export
   student records, or view the dashboard.

---

## 🔐 Login & Security

- A default admin account (`admin` / `admin123`) is created
  automatically the first time you run the program.
- Passwords are **never stored in plain text** — they are hashed with
  SHA-256 before being saved to the database.
- You get **3 login attempts** before the program exits.
- Use menu option **9 (Change Password)** to set your own password
  after logging in for the first time.
- ⚠️ Note: SHA-256 is used here for simplicity and to avoid extra
  dependencies. In a real production system, a slower, salted
  algorithm like **bcrypt** or **Argon2** (designed specifically for
  passwords) should be used instead.

---

## 🗄 SQL Queries Used

**Create Students Table**
```sql
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
```

**Create Admins Table (Login System)**
```sql
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
```

**Insert (Add Student)**
```sql
INSERT INTO students
    (name, dob, age, gender, department, semester,
     phone, email, address, photo_path, admission_date)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
```

**Select All (View Students)**
```sql
SELECT * FROM students ORDER BY id ASC;
```

**Count**
```sql
SELECT COUNT(*) FROM students;
```

**Search by ID**
```sql
SELECT * FROM students WHERE id = ?;
```

**Search by Name (partial match)**
```sql
SELECT * FROM students WHERE name LIKE ?;
```

**Update**
```sql
UPDATE students
SET name = ?, dob = ?, age = ?, gender = ?, department = ?,
    semester = ?, phone = ?, email = ?, address = ?,
    photo_path = ?, admission_date = ?
WHERE id = ?;
```

**Delete**
```sql
DELETE FROM students WHERE id = ?;
```

**Dashboard — Group Counts (example: by department)**
```sql
SELECT department, COUNT(*) as total
FROM students
GROUP BY department
ORDER BY total DESC;
```

**Login Verification**
```sql
SELECT password_hash FROM admins WHERE username = ?;
```

> All queries use **parameterized placeholders (`?`)** instead of string
> concatenation/formatting, which protects the application against
> SQL injection attacks.

---

## 🖥 Example Output (Text-Based)

**Login Screen**
```
==============================
   STUDENT MANAGEMENT SYSTEM
         ADMIN LOGIN
==============================
Username: admin
Password: admin123

[SUCCESS] Welcome, admin!
```

**Main Menu**
```
==============================
 STUDENT MANAGEMENT SYSTEM
     Logged in as: admin
==============================
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Count Students
7. Dashboard
8. Export to CSV
9. Change Password
10. Logout / Exit
==============================
Enter your choice (1-10):
```

**Adding a Student**
```
----- ADD NEW STUDENT -----
Enter Name: Rohan Sharma
Enter Date of Birth (YYYY-MM-DD): 2005-06-15
Enter Gender (Male/Female/Other): Male
Enter Department (e.g., AIDS, CSE, MECH): AIDS
Enter Semester (1-8): 3
Enter Phone Number (10 digits): 9876543210
Enter Email: rohan@example.com
Enter Address: 221B Baker Street, Pune
Enter Photo File Path (optional, press Enter to skip):
Enter Admission Date (YYYY-MM-DD, press Enter for today):

[SUCCESS] Student 'Rohan Sharma' added successfully with ID 1.
```

**Dashboard**
```
==============================
           DASHBOARD
==============================

Total Students : 2
Average Age    : 21.0 years

Students by Department:
   CSE          | ############################## (1)
   AIDS         | ############################## (1)

Students by Gender:
   Male         | ############################## (1)
   Female       | ############################## (1)

Students by Semester:
   3            | ############################## (1)
   5            | ############################## (1)
```

**Exporting to CSV**
```
----- EXPORT TO CSV -----

[SUCCESS] Exported 2 record(s) to:
          .../students_export_20260712_103555.csv
```

**Searching by ID (full detail view)**
```
---------------------------------------------
Student ID     : 1
Name           : Rohan Sharma
Date of Birth  : 2005-06-15
Age            : 21
Gender         : Male
Department     : AIDS
Semester       : 3
Phone          : 9876543210
Email          : rohan@example.com
Address        : 221B Baker Street, Pune
Photo Path     : N/A
Admission Date : 2026-07-12
---------------------------------------------
```

---

## 📄 File-by-File Explanation

- **`main.py`** — The program's entry point. Initializes the database,
  requires a successful login, then runs the main menu loop, dispatching
  each user choice to the correct function via a dictionary lookup.

- **`database.py`** — Contains `get_connection()`, and creates both the
  `students` table (with the new DOB/address/photo/admission fields)
  and the `admins` table, seeding a default admin account on first run.

- **`auth.py`** — The login system. Hashes passwords with SHA-256,
  verifies credentials, limits login attempts, and lets an admin
  change their password.

- **`colors.py`** — Centralized helpers (`print_success`, `print_error`,
  `print_warning`, `print_info`, `print_header`, `print_title`) built
  on top of `colorama`, with a safe no-color fallback if it isn't installed.

- **`utils.py`** — Shared helper functions: input validators (including
  `validate_date_format` and `calculate_age_from_dob`), input-collection
  helpers, and colored display helpers for tables and single-record views.

- **`add_student.py`** — Collects and validates a new student's details
  (including DOB, address, photo path, admission date), then inserts
  the record into the database. Age is calculated automatically from DOB.

- **`view_student.py`** — Fetches and displays all students in a
  colored table, and provides a function to count total students.

- **`search_student.py`** — Lets the user search by Student ID (exact
  match) or Name (partial match using SQL `LIKE`).

- **`update_student.py`** — Shows a student's current details and lets
  the user update any field. If DOB changes, Age is recalculated
  automatically to keep the two fields consistent.

- **`delete_student.py`** — Deletes a student record after showing
  their details and asking for explicit confirmation.

- **`dashboard.py`** — Displays total students, average age, and
  simple text-based bar charts for breakdowns by department, gender,
  and semester.

- **`export_data.py`** — Exports all student records to a timestamped
  CSV file that can be opened in Excel or Google Sheets.

---

## 🚀 Future Enhancements

- Add a **GUI** using Tkinter or PyQt for a more user-friendly experience.
- Build a **web version** using Flask/Django with HTML templates.
- Store and **display actual photo thumbnails** (currently only a
  file-path reference is stored, since this is a terminal app).
- Add **multiple admin roles** (e.g., super-admin vs. read-only staff).
- Switch to **bcrypt/Argon2** password hashing for production use.
- Add **pagination** for viewing large numbers of records.
- Add **sorting/filtering** options (by department, semester, age, etc.).
- Add **unit tests** using `unittest` or `pytest`.
- Add **data backup/restore** functionality.
- Add **attendance and grades** management modules.
- Export the dashboard as a **PDF report**.

---

## 👤 Author

Built as a mini-project for academic purposes — feel free to fork,
modify, and extend this project for your own learning or coursework.

---

## 📃 License

This project is free to use for educational purposes.
