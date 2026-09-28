"""
main.py
Entry point: shows the menu, reads user input, calls the functions
in student_operations.py and prints the results.
Run with:  python main.py
"""
from database import create_table
import student_operations as ops


# ---------- input helpers (validation) ----------
def read_text(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("  This field cannot be empty.")


def read_roll(prompt="Roll number: "):
    while True:
        text = input(prompt).strip()
        try:
            roll = int(text)
        except ValueError:
            print("  Roll number must be a whole number.")
            continue
        if roll > 0:
            return roll
        print("  Roll number must be greater than 0.")


def read_marks(prompt="Marks (0-100): "):
    while True:
        text = input(prompt).strip()
        try:
            marks = float(text)
        except ValueError:
            print("  Marks must be a number.")
            continue
        if 0 <= marks <= 100:
            return marks
        print("  Marks must be between 0 and 100.")


# ---------- output helper ----------
def print_students(rows):
    if not rows:
        print("  No records found.")
        return
    print(f"\n  {'Roll':<8}{'Name':<22}{'Dept':<10}{'Marks':>7}")
    print("  " + "-" * 47)
    for roll, name, dept, marks in rows:
        print(f"  {roll:<8}{name:<22}{dept:<10}{marks:>7.2f}")
    print()


# ---------- menu actions ----------
def add_student_flow():
    roll = read_roll()
    name = read_text("Name: ").title()
    dept = read_text("Department (e.g. CSE): ").upper()
    marks = read_marks()
    ok, message = ops.add_student(roll, name, dept, marks)
    print("  " + message)


def search_by_roll_flow():
    student = ops.get_student_by_roll(read_roll())
    print_students([student] if student else [])


def search_by_department_flow():
    dept = read_text("Department: ").upper()
    print_students(ops.get_students_by_department(dept))


def update_marks_flow():
    roll = read_roll()
    marks = read_marks("New marks (0-100): ")
    ok, message = ops.update_marks(roll, marks)
    print("  " + message)


def delete_flow():
    roll = read_roll()
    student = ops.get_student_by_roll(roll)
    if not student:
        print(f"  No student found with roll number {roll}.")
        return
    confirm = input(f"  Delete {student[1]}? (y/n): ").strip().lower()
    if confirm == "y":
        ok, message = ops.delete_student(roll)
        print("  " + message)
    else:
        print("  Deletion cancelled.")


def statistics_flow():
    s = ops.get_statistics()
    if s["total"] == 0:
        print("  No records yet.")
        return
    print(f"\n  Total students : {s['total']}")
    print(f"  Average marks  : {s['average']:.2f}")
    print(f"  Highest marks  : {s['highest']:.2f}")
    print(f"  Lowest marks   : {s['lowest']:.2f}")
    print(f"  Topper         : {s['topper'][0]} ({s['topper'][1]:.2f})\n")


def query_plan_flow():
    for label, sql, plan in ops.get_query_plans():
        print(f"\n  {label}")
        print(f"    SQL : {sql}")
        for line in plan:
            print(f"    Plan: {line}")
    print()


MENU = """
====== Student Database Management System ======
 1. Add student
 2. View all students
 3. Search by roll number
 4. Search by department
 5. Update marks
 6. Delete student
 7. Class statistics
 8. Show query plans (learning demo)
 0. Exit
"""

ACTIONS = {
    "1": add_student_flow,
    "2": lambda: print_students(ops.get_all_students()),
    "3": search_by_roll_flow,
    "4": search_by_department_flow,
    "5": update_marks_flow,
    "6": delete_flow,
    "7": statistics_flow,
    "8": query_plan_flow,
}


def main():
    create_table()  # make sure the table exists before anything else
    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("  Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()

