import sqlite3
from contextlib import contextmanager
from security_logic import hash_password, encrypt_data

DB_NAME = "database.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cur = conn.cursor()

        # Users table now includes email and role is NOT NULL
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        # Applications table includes secret_note
        cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            first_name TEXT,
            last_name TEXT,
            job TEXT,
            school TEXT,
            department TEXT,
            salary TEXT,
            secret_note TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

def insert_user(first_name, last_name, email, password, role="Candidate"):
    hashed_password = hash_password(password)
    with get_db() as conn:
        try:
            conn.execute("""
            INSERT INTO users (first_name, last_name, email, password, role)
            VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, email, hashed_password, role))
            return True
        except sqlite3.IntegrityError:
            return False

def update_user_role(user_id, new_role):
    with get_db() as conn:
        conn.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))

def get_user_by_email(email):
    with get_db() as conn:
        return conn.execute("""
        SELECT * FROM users
        WHERE email = ?
        """, (email,)).fetchone()

def get_user_by_id(user_id):
    with get_db() as conn:
        return conn.execute("""
        SELECT * FROM users
        WHERE id = ?
        """, (user_id,)).fetchone()

def insert_application(user_id, first_name, last_name, job, school, department, salary):
    encrypted_school = encrypt_data(school)
    encrypted_department = encrypt_data(department)
    encrypted_salary = encrypt_data(salary)
    with get_db() as conn:
        conn.execute("""
        INSERT INTO applications
        (user_id, first_name, last_name, job, school, department, salary, secret_note)
        VALUES (?, ?, ?, ?, ?, ?, ?, NULL)
        """, (user_id, first_name, last_name, job, encrypted_school, encrypted_department, encrypted_salary))

def get_application_by_user(user_id):
    with get_db() as conn:
        return conn.execute("SELECT * FROM applications WHERE user_id = ?", (user_id,)).fetchone()

def get_all_applications():
    with get_db() as conn:
        return conn.execute("SELECT * FROM applications").fetchall()

def update_application_note(app_id, note):
    with get_db() as conn:
        conn.execute("UPDATE applications SET secret_note = ? WHERE id = ?", (note, app_id))