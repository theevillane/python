import hashlib
import re
from pymongo import MongoClient
from getpass import getpass
import os

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

def connect_to_mongo():
    """Connect to the MongoDB database with error handling."""
    try:
        client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))  # Use environment variable for MongoDB URI
        print("Connected to MongoDB.")
        return client["attendance_db"]  # Replace with your database name
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None

def save_attendance_to_mongo(attendance_list, username):
    """Save or update the attendance list to MongoDB."""
    db = connect_to_mongo()
    if db:
        collection = db["attendance"]  # Replace with your collection name
        attendance_entry = {
            "username": username,
            "attendance": attendance_list
        }
        collection.update_one({"username": username}, {"$set": attendance_entry}, upsert=True)
        print("Attendance list has been saved or updated in MongoDB.")
    else:
        print("Could not save to MongoDB. Check connection.")

def register_user(users, admin_users):
    """Register a new user with role and password validation."""
    ADMIN_CONFIRM_PASSWORD = os.getenv("ADMIN_CONFIRM_PASSSWORD", "secureAdminPass") #Admin confirmation password for added security

    username = input("Enter a username: ").lower()
    if username in users or username in admin_users:
        print("Username already exists. Try a different one.")
        return

    password = getpass("Enter a password: ")
    if not is_strong_password(password):
        print("Password is weak. Please choose a stronger password.")
        return
    
    is_admin = input("Is this user an admin? (yes/no): ").strip().lower() == 'yes'
    #hashed_password = hash_password(password)
    if is_admin:
        confirm_admin_password = getpass("Enter the admin confirmation password: ")
        if hash_password(confirm_admin_password) != hash_password(ADMIN_CONFIRM_PASSWORD):
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
    password = getpass("Enter your password: ")
    hashed_password = hash_password(password)

    if username in users and users[username] == hashed_password:
        print(f"Welcome, {username}!")
        return username, False
    elif username in admin_users and admin_users[username] == hashed_password:
        print(f"Welcome, Admin {username}!")
        return username, True
    else:
        print("Invalid username or password. Please try again.")
        return None, None

def record_attendance(users, admin_users):
    """Main function to handle the attendance system."""
    attendance_list = []

    while True:
        print("\n1. Sign Up")
        print("2. Login")
        print("3. Exit")
        user_choice = input("Choose an option (1-3): ")

        if user_choice == '1':
            register_user(users, admin_users)
        
        elif user_choice == '2':
            username, is_admin = login_user(users, admin_users)
            if username is None:
                continue

            while True:
                print("\nAttendance Menu")
                print("1. Add Your Name (Student)")
                if is_admin:
                    print("2. Add Student (Admin Only)")
                    print("3. Delete Student")
                print("4. View Attendance List")
                print("5. Save Attendance to MongoDB")
                print("6. Log Out")

                menu_choice = input("Choose an option: ")

                if menu_choice == '1':
                    name = username.upper()
                    if name in map(str.upper, attendance_list):
                        print(f"{name} is already in the attendance list.")
                    else:
                        attendance_list.append(name)
                        print(f"{name} has been added to the attendance list.")

                elif menu_choice == '2' and is_admin:
                    name = input("Enter the student's name to add: ").upper()
                    if name in map(str.upper, attendance_list):
                        print(f"{name} is already in the attendance list.")
                    else:
                        attendance_list.append(name)
                        print(f"{name} has been added to the attendance list.")

                elif menu_choice == '3' and is_admin:
                    name = input("Enter the student's name to delete: ").upper()
                    if name in attendance_list:
                        attendance_list.remove(name)
                        print(f"{name} has been deleted from the attendance list.")
                    else:
                        print(f"{name} is not in the attendance list.")

                elif menu_choice == '4':
                    if attendance_list:
                        print("\nAttendance List:")
                        for idx, student in enumerate(attendance_list, start=1):
                            print(f"{idx}. {student}")
                    else:
                        print("No students have attended yet.")

                elif menu_choice == '5':
                    save_attendance_to_mongo(attendance_list, username)

                elif menu_choice == '6':
                    confirm_logout = input("Are you sure you want to logout? yes/no")
                    if confirm_logout == 'yes':
                         print("Logging out.")
                         break
                    else:
                        print("Logout cancelled.")

                else:
                    print("Invalid option. Please choose a valid number.")

        elif user_choice == '3':
            confirm_exit = input("Are you sure you want to exit? yes/no: ").strip().lower()
            if confirm_exit():
                print("Exiting the Program.")
                break

        else:
            print("Invalid option. Please choose a number between 1 and 3.")

# Set up environment and initialize the attendance system
os.environ["MONGO_URI"] = "mongodb://localhost:27017/"  # Set MongoDB URI in environment variable
users = {}  # Dictionary to store usernames and hashed passwords
admin_users = {}  # Dictionary for admin users

# Run the attendance recorder
record_attendance(users, admin_users)
