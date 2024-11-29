import hashlib
import re
from openpyxl import Workbook, load_workbook
from getpass import getpass
import os
import logging
import time



logging.basicConfig(
    filename='app_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def initialize_excel():
    """Create excel file with the necessary sheets and headers."""
    if not os.path.exists("attendance_db.xlsx"):
        wb = Workbook()

        # User sheet
        users_sheet = wb.active
        users_sheet.title = "Users"
        users_sheet.append(["Username", "Password", "Role"])

        # Attendance sheet
        attendance_list = wb.create_sheet("Attendance")
        attendance_list.append(["Username", "Attendance"])

        wb.save("attendance_db.xlsx")
        print("Excel db initialized.")

def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong_password(password):
    """Check if the password is strong."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def add_to_attendance_list(username, attendance_list):
    """Add a username to the attendance list."""
    name = input("Enter the student's name to add: ").strip().upper()

    name = username.upper()
    if name in attendance_list:
        print(f"{name} is already in the attendance list.")
    else:
        attendance_list.append(name)
        print(f"{name} has been added to the attendance list.")
    default_password = "Password@123"
    hashed_password = hash_password(default_password)
    add_user_to_excel(name, hashed_password, "user")
    print(f"Student '{name}' has also been added to users sheet with a default password.")

def remove_from_attendance_list(attendance_list):
    """Remove a name from the attendance list."""
    name = input("Enter the student's name to delete: ").upper()

    if name in attendance_list:
        attendance_list.remove(name)
        print(f"{name} has been removed from the attendance list.")
    else:
        print(f"{name} is not in the attendance list.")


def save_attendance_to_excel(attendance_list, username):
    """Save or update the attendance list to excel file."""
    try:
        wb = load_workbook("attendance_db.xlsx")
        sheet = wb["Attendance"]
        for student in attendance_list:
            found = False
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if student == row[0]:
                    found = True
                    break
            if not found:
                sheet.append([student])
        wb.save("attendance_db.xlsx")
        print("Attendance list saved to excel")
    except Exception as e:
        print(f"Error saving attendance: {e}")



def get_user_role(username, hashed_password):
    """Retrieve the role of a user based on username and hashed password."""
    try:
        wb = load_workbook("attendance_db.xlsx")
        sheet = wb["Users"]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0].lower() == username.lower() and row[1] == hashed_password:
                return row[2]  # Return role (e.g., 'admin' or 'user')
        return None
    except Exception as e:
        logging.error(f"Error retrieving user role: {e}")
        return None

def validate_login(username, hashed_password):
    """Validate a user's login credentials from the Excel file."""
    try:
        wb = load_workbook("attendance_db.xlsx")
        sheet = wb["Users"]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            logging.debug(f"Checking row: username={row[0]}, stored_hashed_password={row[1]}, role={row[2]}")
            if row[0].lower() == username.lower() and row[1] == hashed_password:
                logging.debug(f"Match found: {row}")
                return row[2]  # Return the role ('admin' or 'user')
        print("Login failed. Username or password mismatch.")
        return None
    except Exception as e:
        print(f"Error validating login: {e}")
        return None

def add_user_to_excel(username, hashed_password, role):
    """Add a new user to the Users sheet in Excel."""
    try:
        wb = load_workbook("attendance_db.xlsx")
        sheet = wb["Users"]

        # Check if the user already exists
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0].lower() == username.lower():
                print("Username already exists. Try a different one.")
                return

        # Add the user
        sheet.append([username, hashed_password, role])
        wb.save("attendance_db.xlsx")
        print(f"User '{username}' added successfully.")
    except Exception as e:
        print(f"Error adding user: {e}")

def view_attendance_from_excel():
    """Display the attendance list from Excel."""
    try:
        wb = load_workbook("attendance_db.xlsx")
        sheet = wb["Attendance"]
        print("\nAttendance List:")
        for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=1):
            print(f"{idx}. {row[0]} - {row[1]}")
    except Exception as e:
        print(f"Error viewing attendance: {e}")

def register_user(users, admin_users):
    """Register a new user with role and password validation."""
    ADMIN_CONFIRM_PASSWORD_HASH = hash_password(os.getenv("ADMIN_CONFIRM_PASSWORD", "Kijanamdogo"))  # Admin confirmation password for added security

    username = input("Enter a username: ").lower()
    if username in users or username in admin_users:
        print("Username already exists. Try a different one.")
        return

    # Check password strength
    password = getpass("Enter a password: ")
    if not is_strong_password(password):
        print("Password is weak. Please choose a stronger password.")
        return

    is_admin = input("Is this user an admin? (yes/no): ").strip().lower() == 'yes'
    hashed_password = hash_password(password)
    role = "admin" if is_admin else "user"
    add_user_to_excel(username, hashed_password, role)

    if is_admin:
        confirm_admin_password = getpass("Enter the admin confirmation password: ")
        if hash_password(confirm_admin_password) != ADMIN_CONFIRM_PASSWORD_HASH:
            print("Admin confirmation password is incorrect. Registration failed.")
            return

        admin_users[username] = hash_password(password)
        print("Admin registration successful!")
    else:
        users[username] = hash_password(password)
        print("User registration successful!")

def login_user(users, admin_users):
    """Log in a user and return username and role."""
    username = input("Enter your username: ").lower()
    if username in users or username in admin_users:
        print("User already exixst. Try a different one.")
    password = getpass("Enter your password: ")
    hashed_password = hash_password(password)  # Ensure password is hashed before validation

    role = validate_login(username, hashed_password)

    if role:
        print(f"Welcome, {username}! You are an {role}")
        return username, role
    else:
        print("Invalid username or password.")
        return None, None


def reset_password():
    """Reset a user's password."""
    try:
        wb = load_workbook("attendance_db.xlsx")
        sheet = wb["Users"]
        
        username = input("Enter the username for password reset: ").strip().lower()
        user_found = False

        for row in sheet.iter_rows(min_row=2, max_col=3, values_only=False):
            if row[0].value.lower() == username:
                user_found = True

                # If admin is resetting, ask for confirmation
                is_admin_reset = input("Are you an admin resetting this password? (yes/no): ").strip().lower() == 'yes'
                if is_admin_reset:
                    admin_password = getpass("Enter the admin confirmation password: ")
                    admin_hash = hash_password(os.getenv("ADMIN_CONFIRM_PASSWORD", "Kijanamdogo"))
                    if hash_password(admin_password) != admin_hash:
                        print("Admin confirmation failed. Password reset aborted.")
                        return

                # Prompt for a new password
                new_password = getpass("Enter the new password: ")
                if not is_strong_password(new_password):
                    print("The password is too weak. Please choose a stronger one.")
                    return

                # Update the password
                row[1].value = hash_password(new_password)
                wb.save("attendance_db.xlsx")
                print("Password reset successfully.")
                return

        if not user_found:
            print("Username not found in the system.")
    except Exception as e:
        print(f"Error during password reset: {e}")



def confirm_exit():
    """Confirm if the user wants to exit the program."""
    confirm = input("Are you sure you want to exit? yes/no: ").strip().lower()
    if confirm == 'yes':
        print("Exiting the Program.")
        return True


def record_attendance(users, admin_users):
    """Main function to handle the attendance system."""
    attendance_list = []

    while True:
        print()
        local_time = time.localtime()
        print(f"It is {local_time.tm_year}, {local_time.tm_mon}, {local_time.tm_mday}   Time:{local_time.tm_hour}:{local_time.tm_min}:{local_time.tm_sec}")
        print("Welcome to our class today.")
        print("Make sure you login to the class and add your name to the attendance list.")
        print("\n1. Register User")
        print("2. Login")
        print("3. View Attendance")
        print("4. Reset Password")
        print("5. Exit")
        user_choice = input("Choose an option (1-5): ")

        if user_choice == '1':
            register_user(users, admin_users)

        elif user_choice == '2':
            username, role = login_user(users, admin_users)
            if role:
                is_admin = (role == "admin")
                while True:
                    print("\nAttendance Menu")
                    print("1. Add Your Name (Student)")
                    if is_admin:
                        print("2. Add Student (Admin Only)")
                        print("3. Delete Student")
                    print("4. View Attendance List")
                    print("5. Save Attendance")
                    print("6. Log Out")

                    menu_choice = input("Choose an option: ")

                    if menu_choice == '1':
                        if is_admin:
                            print("Error: Admins cannot add their name to the attendance list.")
                        else:
                            name = username.upper()
                            if name in map(str.upper, attendance_list):
                                print(f"{name} is already in the attendance list.")
                            else:
                                attendance_list.append(name)
                                print(f"{name} has been added to the attendance list.")

                    elif menu_choice == '2' and is_admin:
                        add_to_attendance_list(username,attendance_list)

                    elif menu_choice == '3' and is_admin:
                        remove_from_attendance_list(attendance_list)

                    elif menu_choice == '4':
                        view_attendance_from_excel()

                    elif menu_choice == '5':
                        save_attendance_to_excel(attendance_list, username)

                    elif menu_choice == '6':
                        confirm_logout = input("Are you sure you want to logout? yes/no: ").strip().lower()
                        if confirm_logout == 'yes':
                            print("Logging out.")
                            break
                        else:
                            print("Logout cancelled.")

                    else:
                        print("Invalid option. Please choose a valid number.")

        elif user_choice == '3':
            view_attendance_from_excel()
        
        elif user_choice == '4':
            reset_password()

        elif user_choice == '5':
            if confirm_exit():
                break

        else:
            print("Invalid option. Please choose a number between 1 and 4.")

if __name__ == "__main__":
    initialize_excel()  
    record_attendance({}, {})  

users = {}  # Dictionary to store usernames and hashed passwords
admin_users = {}  # Dictionary for admin users

# Run the attendance recorder
record_attendance(users, admin_users)
