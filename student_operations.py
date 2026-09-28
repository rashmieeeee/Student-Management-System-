"""
student_operations.py
All SQL lives here: Create, Read, Update, Delete (CRUD) + statistics.
Every query uses '?' placeholders so user input can never change the SQL
(this prevents SQL injection).
"""
import sqlite3
from database import get_connection


# ---------- CREATE ----------
def add_student(roll_number, name, department, marks):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO students (roll_number, name, department, marks) "
            "VALUES (?, ?, ?, ?)",
            (roll_number, name, department, marks),
        )
        conn.commit()
        return True, "Student added successfully."
    except sqlite3.IntegrityError:
        # Primary key rule broken: this roll number already exists
        return False, f"Roll number {roll_number} already exists."
    finally:
        conn.close()


# ---------- READ ----------
def get_all_students():
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT roll_number, name, department, marks "
            "FROM students ORDER BY roll_number"
        )
        return cur.fetchall()  # list of tuples
    finally:
        conn.close()


def get_student_by_roll(roll_number):
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT roll_number, name, department, marks "
            "FROM students WHERE roll_number = ?",
            (roll_number,),
        )
        return cur.fetchone()  # one tuple, or None if not found
    finally:
        conn.close()


def get_students_by_department(department):
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT roll_number, name, department, marks "
            "FROM students WHERE department = ? ORDER BY roll_number",
            (department,),
        )
        return cur.fetchall()
    finally:
        conn.close()


# ---------- UPDATE ----------
def update_marks(roll_number, new_marks):
    conn = get_connection()
    try:
        cur = conn.execute(
            "UPDATE students SET marks = ? WHERE roll_number = ?",
            (new_marks, roll_number),
        )
        conn.commit()
        if cur.rowcount == 0:  # no row matched the WHERE condition
            return False, f"No student found with roll number {roll_number}."
        return True, "Marks updated successfully."
    finally:
        conn.close()


# ---------- DELETE ----------
def delete_student(roll_number):
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM students WHERE roll_number = ?", (roll_number,)
        )
        conn.commit()
        if cur.rowcount == 0:
            return False, f"No student found with roll number {roll_number}."
        return True, "Student deleted successfully."
    finally:
        conn.close()


# ---------- STATISTICS (aggregate functions) ----------
def get_statistics():
    conn = get_connection()
    try:
        total, avg, highest, lowest = conn.execute(
            "SELECT COUNT(*), AVG(marks), MAX(marks), MIN(marks) FROM students"
        ).fetchone()
        topper = conn.execute(
            "SELECT name, marks FROM students ORDER BY marks DESC LIMIT 1"
        ).fetchone()
        return {
            "total": total,
            "average": avg,
            "highest": highest,
            "lowest": lowest,
            "topper": topper,
        }
    finally:
        conn.close()


# ---------- QUERY OPTIMIZATION DEMO ----------
def get_query_plans():
    """Ask SQLite HOW it will run three queries (EXPLAIN QUERY PLAN)."""
    queries = [
        ("Search by roll number (primary key)",
         "SELECT * FROM students WHERE roll_number = 1"),
        ("Search by department (has an index)",
         "SELECT * FROM students WHERE department = 'CSE'"),
        ("Search by marks (no index)",
         "SELECT * FROM students WHERE marks > 80"),
    ]
    conn = get_connection()
    try:
        results = []
        for label, sql in queries:
            rows = conn.execute("EXPLAIN QUERY PLAN " + sql).fetchall()
            results.append((label, sql, [row[3] for row in rows]))
        return results
    finally:
        conn.close()

