import hashlib
import re
from pymongo import MongoClient

def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong_password(password):
    """Check if the password is strong."""
    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def connect_to_mongo():
    """Connect to the MongoDB database."""
    client = MongoClient("mongodb://localhost:27017/") #Update with yor MongoDb URI
    return client["attendance_db"] #Replace with your database name

def save_attendance_to_mongo(attendance_list, username):
    """Save the attendance list to MongoDB."""
    db = connect_to_mongo()
    collection = db["attendance"] #Replace with your collection name
    attendance_entry = {
        "username": username,
        "attendance": attendance_list
    }
    collection.insert_one(attendance_entry)

    # Load existing attendance from file if available.
#def load_attendance():
 #   try:
  #      with open('attendance_list.txt', 'r') as file:
   #         return [line.strip() for line in file.readlines()]
    #except FileNotFoundError:
     #   return[] # File does not exist; start with an empty list

    
def record_attendance():
    # Initialize attendance list and user credentials
    attendance_list = []
    users = {}  # Dictionary to store usernames and hashed passwords
    admin_users = {}  # Dictionary for admin users

    admin_password = "admin1234"  # Set a fixed password for admin


    while True:
        print("\n1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            # User registration
            username = input("Enter a username: ").lower()
            if username in users or username in admin_users:
                print("Username already exists. Try a different one.")
            else:
                password = input("Enter a password: ")
                if not is_strong_password(password):
                    print("Password is weak. please choose a stronger password.")
                    continue #go back to registration prompt
                is_admin = input("Is this user an admin? (yes/no): ").strip().lower() == 'yes'
                if is_admin:
                    admin_users[username] = hash_password(password)  # Store admin user
                    print("Admin registration successful!")
                else:
                    users[username] = hash_password(password)  # Store regular user
                    print("User registration successful!")
        
        elif choice == '2':
            # User authentication
            username = input("Enter your username: ").lower()
            password = input("Enter your password: ")
            hashed_password = hash_password(password)

            if username in users and users[username] == hashed_password:
                print(f"Welcome, {username}!")
                logged_in_user = username
                is_admin = False
            elif username in admin_users and admin_users[username] == hashed_password:
                print(f"Welcome, Admin {username}!")
                logged_in_user = username
                is_admin = True
            else:
                print("Invalid username or password. Please try again.")
                continue

            # Start attendance recording
            while True:
                print("\nAttendance List")
                print("-------------------")
                print("1. Add Your name(Student)")

                #show admin only options if the user is admin
                if is_admin:
                    print("2. Add Student (Admin Only)")
                    print("3. Delete Student")
                    counts = 4
                else:
                    counts = 3

                
                print(f"{counts}. View attendance list")
                print(f"{counts + 1}. Save Attendance to File")
                print(f"{counts + 1 +1}. Exit")
                
                    
                choice = input(f"Choose an option (1-{counts + 1 +1}): ")

                if choice == '1':
                    # Add the logged-in user's name to the attendance list
                    name = logged_in_user.upper()
                    if name in map(str.upper, attendance_list):
                        print(f"Sorry! {name} is already in the attendance list.")
                    else:
                        attendance_list.append(name)
                        print(f"{name} has been added to the attendance list.")
                
                
                elif choice == '2' and is_admin:
                    #Adds student by name
                    name = input("Enter the student's name to add: ").upper()
                    if name in map(str.upper, attendance_list):
                        print(f"Sorry! {name} is already in the attendance list.")
                    else:
                        attendance_list.append(name)
                        print(f"{name} has been added to the attendance list.")

                elif choice == str(counts):
                    # View the attendance list
                    if attendance_list:
                        print("\nAttendance List:")
                        for index, student in enumerate(attendance_list, start=1):
                            print(f"{index}. {student}")
                    else:
                        print("No students have attended the event yet.")

                elif choice == str(counts + 1):
                    # Save attendance list to MongoDB
                    save_attendance_to_mongo(attendance_list, logged_in_user)
                    print("Attendance list has been saved to MongoDB.")

                elif choice == str(counts + 1 + 1):
                    # Exit the program
                    confirm_exit = input("Are you sure you want to exit? (yes/no): ").strip().lower()
                    if confirm_exit == 'yes':
                        print("Exiting the attendance recorder.")
                        break

                elif choice == '3' and is_admin:
                    # Delete a student from the attendance list.
                    name = input("Enter the student name to delete: ").upper()
                    if name in attendance_list:
                        attendance_list.remove(name)
                        print(f"{name} has been deleted from the attendance list")
                    else:
                        print(f"{name} is not in the attendance list")
                else:
                    print("Invalid option. Please choose a number between 1 and 5.")

        elif choice == '3':
            confirm_exit = input("Are you sure you want to exit? (yes/no): ").strip().lower()
            if confirm_exit == 'yes':
                print("Exiting the Program.")
                break

        else:
            print("Invalid option. Please choose a number between 1 and 3.")

# Run the attendance recorder
record_attendance()
