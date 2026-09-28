"""
database.py
Handles the database connection and creates the table.
Uses only Python's built-in sqlite3 module (no installation needed).
"""
import sqlite3

DB_NAME = "students.db"  # SQLite stores everything in this single file


def get_connection():
    """Open a connection to the database file (the file is created if missing)."""
    return sqlite3.connect(DB_NAME)


def create_table():
    """Create the students table and an index. Safe to run every time the app starts."""
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                roll_number INTEGER PRIMARY KEY,
                name        TEXT NOT NULL,
                department  TEXT NOT NULL,
                marks       REAL NOT NULL CHECK (marks >= 0 AND marks <= 100)
            )
            """
        )
        # Index makes "search by department" fast (explained in the guide)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_students_department "
            "ON students(department)"
        )
        conn.commit()
    finally:
        conn.close()

