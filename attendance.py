import hashlib
import re

def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong_password(password):
    """Check if the password meets the strength requirements."""
    if (len(password) < 8 or
        not re.search(r"[A-Za-z]", password) or  # At least one letter
        not re.search(r"[0-9]", password) or  # At least one digit
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):  # At least one special character
        return False
    return True

def load_attendance():
    """Load existing attendance from a file."""
    try:
        with open('attendance_list.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []  # File does not exist; start with an empty list

def load_users():
    """Load existing users from a file."""
    try:
        with open('users.txt', 'r') as file:
            return {line.split()[0]: line.split()[1] for line in file.readlines()}
    except FileNotFoundError:
        return {}  # No users yet

def save_users(users):
    """Save users to a file."""
    with open('users.txt', 'w') as file:
        for username, password in users.items():
            file.write(f"{username} {password}\n")

def record_attendance():
    # Initialize attendance list and user credentials
    attendance_list = load_attendance()
    users = load_users()  # Load users from file
    admin_users = {}  # Dictionary for admin users

    while True:
        print("\n1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            # User registration
            username = input("Enter a username: ").lower()
            if username in users:
                print("Username already exists. Try a different one.")
            else:
                password = input("Enter a password: ")
                if not is_strong_password(password):
                    print("Password must be at least 8 characters long, include letters, numbers, and special characters.")
                    continue
                is_admin = input("Is this user an admin? (yes/no): ").strip().lower() == 'yes'
                if is_admin:
                    admin_users[username] = hash_password(password)  # Store admin user
                    print("Admin registration successful!")
                else:
                    users[username] = hash_password(password)  # Store regular user
                    print("User registration successful!")
                save_users(users)  # Save users after registration
        
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
                print("1. Add Student")
                print("2. View Attendance List")
                print("3. Save Attendance to File")
                print("4. Update Password")
                print("5. Exit")
                if is_admin:
                    print("6. Delete Student")
                choice = input("Choose an option (1-6): ")

                if choice == '1':
                    # Add the logged-in user's name to the attendance list
                    name = logged_in_user.upper()
                    if name in map(str.upper, attendance_list):
                        print(f"Sorry! {name} is already in the attendance list.")
                    else:
                        attendance_list.append(name)
                        print(f"{name} has been added to the attendance list.")
                
                elif choice == '2':
                    # View the attendance list
                    if attendance_list:
                        print("\nAttendance List:")
                        for index, student in enumerate(attendance_list, start=1):
                            print(f"{index}. {student}")
                    else:
                        print("No students have attended the event yet.")

                elif choice == '3':
                    # Save attendance list to a file
                    with open('attendance_list.txt', 'w') as file:
                        for student in attendance_list:
                            file.write(f"{student}\n")
                    print("Attendance list has been saved to 'attendance_list.txt'.")

                elif choice == '4':
                    # Update password
                    new_password = input("Enter a new password: ")
                    if not is_strong_password(new_password):
                        print("New password must be strong (at least 8 characters, include letters, numbers, and special characters).")
                        continue
                    users[logged_in_user] = hash_password(new_password)  # Update the password
                    save_users(users)  # Save changes
                    print("Password updated successfully.")

                elif choice == '5':
                    # Exit the program
                    confirm_exit = input("Are you sure you want to exit? (yes/no): ").strip().lower()
                    if confirm_exit == 'yes':
                        print("Exiting the attendance recorder.")
                        break

                elif choice == '6' and is_admin:
                    # Delete a student from the attendance list.
                    name = input("Enter the student name to delete: ").upper()
                    if name in attendance_list:
                        attendance_list.remove(name)
                        print(f"{name} has been deleted from the attendance list")
                    else:
                        print(f"{name} is not in the attendance list")
                else:
                    print("Invalid option. Please choose a number between 1 and 6.")

        elif choice == '3':
            confirm_exit = input("Are you sure you want to exit? (yes/no): ").strip().lower()
            if confirm_exit == 'yes':
                print("Exiting the Program.")
                break

        else:
            print("Invalid option. Please choose a number between 1 and 3.")

# Run the attendance recorder
record_attendance()