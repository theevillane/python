import hashlib

def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def record_attendance():
    # Initialize attendance list and user credentials
    attendance_list = []
    users = {}  # Dictionary to store usernames and hashed passwords
    admin_users = {}  # Dictionary for admin users

    # Load existing attendance from file if available.
    try:
        with open('attendance_list.txt', 'r') as file:
            attendance_list = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        pass  # File does not exist; start with an empty list

    admin_password = "admin1234"  # Set a fixed password for admin

    while True:
        print("\n1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            # User registration
            username = input("Enter a username: ")
            if username in users or username in admin_users:
                print("Username already exists. Try a different one.")
            else:
                password = input("Enter a password: ")
                is_admin = input("Is this user an admin? (yes/no): ").strip().lower() == 'yes'
                if is_admin:
                    admin_users[username] = hash_password(password)  # Store admin user
                    print("Admin registration successful!")
                else:
                    users[username] = hash_password(password)  # Store regular user
                    print("User registration successful!")
        
        elif choice == '2':
            # User authentication
            username = input("Enter your username: ")
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
                print("4. Exit")
                if is_admin:
                    print("5. Delete Student")
                choice = input("Choose an option (1-5): ")

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
                    # Exit the program
                    confirm_exit = input("Are you sure you want to exit? (yes/no): ").strip().lower()
                    if confirm_exit == 'yes':
                        print("Exiting the attendance recorder.")
                        break

                elif choice == '5' and is_admin:
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
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please choose a number between 1 and 3.")

# Run the attendance recorder
record_attendance()
