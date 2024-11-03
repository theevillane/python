import hashlib

def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def record_attendance():
    # Initialize an empty list to store student names and user credentials
    attendance_list = []
    users = {}
    
    # Load existing attendance from file if available.
    try:
        with open('attendance_list.txt', 'r') as file:
            attendance_list = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        pass  # File does not exist; start with an empty list

    admin_password = ["admin123", "owandho254", "123456789"]

    while True:
        print("\n1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            # User registration
            username = input("Enter a username: ")
            if username in users:
                print("Username already exists. Try a different one.")
            else:
                password = input("Enter a password: ")
                users[username] = hash_password(password)
                print("Registration successful!")
        
        elif choice == '2':
            # User authentication
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            hashed_password = hash_password(password)

            if username in users and users[username] == hashed_password:
                print(f"Welcome, {username}!")
                logged_in_user = username

                # Start attendance recording
                while True:
                    print("\nAttendance List")
                    print("-------------------")
                    print("1. Add Student")
                    print("2. View Attendance List")
                    print("3. Save Attendance to File")
                    print("4. Exit")
                    print("5. Delete Student (Admin only)")
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

                    elif choice == '5':
                        # Delete a student from the attendance list.
                        password = input("Enter your admin password: ")
                        if password in admin_password:
                            name = input("Enter the student name to delete: ").upper()
                            if name in attendance_list:
                                attendance_list.remove(name)
                                print(f"{name} has been deleted from the attendance list")
                            else:
                                print(f"{name} is not in the attendance list")
                        else:
                            print("Invalid admin password.")

                    else:
                        print("Invalid option. Please choose a number between 1 and 5.")

            else:
                print("Invalid username or password. Please try again.")

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please choose a number between 1 and 3.")

# Run the attendance recorder
record_attendance()
