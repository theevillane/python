import hashlib
import re
from openpyxl import Workbook, load_workbook
from getpass import getpass
import os
import logging
from datetime import datetime
import random
from functools import wraps
import smtplib
from email.mime.text import MIMEText

logging.basicConfig(
    filename='app_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

EXCEL_FILE = "attendance_db.xlsx"
DEFAULT_PASSWORD = "password123"
ADMIN_CONFIRM_PASSWORD = hashlib.sha256("Kijanamdogo".encode()).hexdigest()

attendance_list = []

def initialize_excel():
    """Create excel file with the necessary sheets and headers."""
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()

        # User sheet
        users_sheet = wb.active
        users_sheet.title = "Users"
        users_sheet.append(["Username", "Password", "Role"])

        # Attendance sheet
        attendance_sheet = wb.create_sheet("Attendance")
        attendance_sheet.append(["Username", "Attendance"])

        wb.save(EXCEL_FILE)
        print("Excel db initialized.")

def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong_password(password):
    """Check if the password is strong."""
    return (len(password) >= 8 and
            re.search(r"[A-Za-z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

def load_sheet(sheet_name):
    """Load a specific sheet from the excel file."""
    try:
        wb = load_workbook(EXCEL_FILE)
        sheet = wb[sheet_name]
        return sheet, wb
    except KeyError:
        print(f"Sheet '{sheet_name}' not found")
    except FileNotFoundError:
        print(f"File '{EXCEL_FILE}' not found.")
    return None, None

def save_to_excel(workbook):
    """Save changes to Excel file."""
    try:
        workbook.save(EXCEL_FILE)
    except Exception as e:
        logging.error(f"Error saving workbook: {e}")

def send_email_notification(to_email, subject, message):
    """Send an email notification with timestamp."""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message += f"\n\nAction Time: {timestamp}"

        from_email = "your_email@example.com"
        from_password = "your_email_password"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())

        print(f"Notification sent to {to_email} at {timestamp}.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def generate_otp():
    """Generate a 6-digit OTP."""
    return random.randint(100000, 999999)

def verify_otp(user_otp, generated_otp):
    """Verify the OTP entered by the user."""
    return user_otp == generated_otp

def require_role(required_role):
    """Decorator to enforce role-based access."""
    def decorator(func):
        @wraps(func)
        def wrapper(username, role, *args, **kwargs):
            if role != required_role:
                print(f"Access denied. You must be a {required_role} to perform this action.")
                return
            return func(username, role, *args, **kwargs)
        return wrapper
    return decorator

def register_user():
    """Register a new user."""
    username = input("Enter a username: ").lower()
    sheet, wb = load_sheet("Users")
    if not sheet:
        print("Error loading user data.")
        return

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[0].lower() == username:
            print("Username already exists. Try a different one.")
            return

    password = getpass("Enter a strong password: ")
    if not is_strong_password(password):
        print("Weak password. Try again.")
        return

    confirm_password = getpass("Confirm your password: ")
    if password != confirm_password:
        print("Passwords do not match. Try again.")
        return

    role = "admin" if input("Is this user an admin? (yes/no): ").strip().lower() == "yes" else "user"
    if role == "admin":
        admin_password = getpass("Enter the admin confirmation password: ")
        if hash_password(admin_password) != ADMIN_CONFIRM_PASSWORD:
            print("Invalid admin confirmation password. Registration failed.")
            return

    hashed_password = hash_password(password)
    sheet.append([username, hashed_password, role])
    save_to_excel(wb)
    print(f"{role.capitalize()} '{username}' registered successfully.")

def login_user():
    """Log in a user and return their username and role."""
    username = input("Enter your username: ").strip().lower()
    password = getpass("Enter your password: ")
    hashed_password = hash_password(password)

    sheet, _ = load_sheet("Users")
    if not sheet:
        print("Error loading user data.")
        return None, None

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[0].lower() == username and row[1] == hashed_password:
            otp = generate_otp()
            print(f"Your OTP is: {otp}")
            user_otp = int(input("Enter the OTP: "))
            if verify_otp(user_otp, otp):
                print(f"Welcome, {username}! You are logged in as {row[2]}.")
                return username, row[2]
            else:
                print("Invalid OTP. Login failed.")
                return None, None

    print("Invalid username or password.")
    return None, None


def add_to_attendance_list(username):
    """Add a student to the attendance list with a timestamp."""
    student_name = input("Enter the student's name to mark attendance: ").strip()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sheet, wb = load_sheet("Attendance")
    if not sheet:
        print("Error loading attendance data.")
        return

    # Append student name and timestamp
    sheet.append([student_name, "Present", timestamp])
    save_to_excel(wb)
    print(f"Attendance marked for {student_name} at {timestamp}.")


@require_role("admin")
def manage_attendance(username, role):
    """Admin-only attendance management."""
    print(f"{username} is managing attendance as {role}.")
    while True:
        print("\nAttendance Management")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. View Attendance")
        print("4. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_to_attendance_list(username)
        elif choice == "2":
            remove_from_attendance_list()
        elif choice == "3":
            view_attendance_from_excel()
        elif choice == "4":
            break
        else:
            print("Invalid option. Try again.")

def log_audit_action(username, action, details=""):
    """Log administrative actions with timestamps."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet, wb = load_sheet("Audit Log")

    # Initialize Audit Log sheet if it doesn't exist
    if not sheet:
        sheet, wb = load_sheet("Audit Log")
        if not sheet:
            print("Error loading audit log.")
            return

        sheet.append(["Timestamp", "Username", "Action", "Details"])

    sheet.append([timestamp, username, action, details])
    save_to_excel(wb)
    logging.info(f"{username} performed action: {action} at {timestamp}. Details: {details}")


def add_to_attendance_list(username):
    """Add a student to the attendance list."""
    student_name = input("Enter the student's name to add: ").strip()
    attendance_list.append(student_name)
    print(f"{student_name} has been added to the attendance list.")
    update_attendance_in_excel(username)

def remove_from_attendance_list():
    """Remove a student from the attendance list."""
    student_name = input("Enter the student's name to remove: ").strip()
    if student_name in attendance_list:
        attendance_list.remove(student_name)
        print(f"{student_name} has been removed from the attendance list.")
    else:
        print(f"{student_name} is not in the attendance list.")

def update_attendance_in_excel(username):
    """Update attendance data in the Excel sheet."""
    sheet, wb = load_sheet("Attendance")
    if not sheet:
        print("Error loading attendance data.")
        return

    sheet.append([username, ", ".join(attendance_list)])
    save_to_excel(wb)
    print("Attendance has been updated in the Excel sheet.")

def view_attendance_from_excel():
    """View attendance records from the Excel sheet."""
    sheet, _ = load_sheet("Attendance")
    if not sheet:
        print("Error loading attendance data.")
        return

    print("\nAttendance Records:")
    for row in sheet.iter_rows(min_row=2, values_only=True):
        print(f"Username: {row[0]}, Attendance: {row[1]}")

def reset_password():
    """Reset a user's password."""
    username = input("Enter the username for password reset: ").strip().lower()
    sheet, wb = load_sheet("Users")
    if not sheet:
        print("Error accessing user data.")
        return

    for row in sheet.iter_rows(min_row=2):
        if row[0].value.lower() == username:
            new_password = getpass("Enter a new password: ")
            if not is_strong_password(new_password):
                print("Weak password. Try again.")
                return
            confirm_password = getpass("Confirm new password: ")
            if new_password != confirm_password:
                print("Passwords do not match.")
                return
            row[1].value = hash_password(new_password)
            save_to_excel(wb)
            print(f"Password for '{username}' has been reset.")
            return

    print("Username not found.")

def main_menu():
    """Main menu for the application."""
    initialize_excel()
    while True:
        print("\nMain Menu")
        print("1. Register User")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            username, role = login_user()
            if username and role:
                if role == "admin":
                    manage_attendance(username, role)
                else:
                    print("Attendance tracking for regular users is under development.")
        elif choice == "3":
            exit = input("Do you wish to exit the program? yes/no: ")
            if exit == 'yes':
                print("Exiting application. Goodbye!")
                break
            else:
              print("Invalid choice. Try again.")
              continue

if __name__ == "__main__":
    main_menu()
