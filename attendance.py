import hashlib

def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()


def record_attendance():
    # Initialize an empty list to store student names
    attendance_list = []
    users = {}
    
    #Load existing attendance from file if available.
    try:
        with open('attendance_list.txt', 'r') as file:
            attendance_list = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        pass #File does not exist; start with an empty list

    admin_password = ["admin123", "owandho254", "123456789"] 

    #users(username, password)
    #users = {"Student1": "password1", "Student2": "password2"}

    #loged_in_user = None

    while True:
        print("\n1. Sign up")
        print("2.Sign in")
        print("3. Exit")
        choice = input("Choose an option(1-3): ")

        if choice == '1':
            #user registration
            username = input("Enter username")
            if username in users:
                print("Username already exists. Try a different one")
            else:
                password =input("Enter a password: ")
                users[username] = hash_password(password)
                print("Registration succesful.")

        elif choice == '2':
            username = ("Enter your username: ")
            password = ("Enmter your password: ")
            hashed_password = hash_password(password)

            if username in users and users[username] == hashed_password:
                print(f"Welcome, {username}!")
                logged_in_user = username



    #while True:
        #if not loged_in_user:
            #print("\nPlease login and continue.")
            #username = input("Enter Username: ")
            #password = input("Enter password:")
            #if username in users and users[username] == password:
             #   loged_in_user = username
              #  print(f"Welcome, {loged_in_user}!")
            #else:
             #   print("Invalid username or password. Try again")
              #  continue
    while True:
        print("\nAttendance List")
        print("-------------------")
        print()    
        print("1. Add Student")
        print("2. View Attendance List")
        print("3. Save Attendance to File")
        print("4. Exit")
        print("5. Delete student (Admin only)")
        choice = input("Choose an option (1-5): ")

        #student name changed to uppercase 
        if choice == '1':
            # Add a student to the attendance list
            name = input("Enter the student's name (or 'back' to return): ").upper()
            if name:
                #check for duplicates
                if name in map(str.upper, attendance_list):
                    print(f"Sorry! {name} is already in the attendance list.")
                else:
                    attendance_list.append(name)
                    print(f"{name} has been added to the attendance list.")
                continue
            
            else:
                print("Name cannot be empty.")
        
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

        #delete input changed to uppercase
        elif choice == '5':
            #Delete a student from the attendance list.
            password = input("Enter your admin password: ")
            if password in admin_password:
                name = input("enter the student name to delete: ").upper()
                if name in attendance_list:
                    attendance_list.remove(name)
                    print(f"{name} has been deleted from the attendance list")
                else:
                    print(f"{name} is not in the attendance list")

        else:
            print("Invalid option. Please choose a number between 1 and 5.")

# Run the attendance recorder
record_attendance()
