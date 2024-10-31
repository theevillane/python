def record_attendance():
    # Initialize an empty list to store student names
    attendance_list = []
    
    #Load existing attendance from file if available.
    try:
        with open('attendance_list.txt', 'r') as file:
            attendance_list = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        pass #File does not exist; start with an empty list

    while True:
        print("\nAttendance Recorder")
        print("-------------------")
        print("1. Add Student")
        print("2. View Attendance List")
        print("3. Save Attendance to File")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            # Add a student to the attendance list
            name = input("Enter the student's name (or 'back' to return): ")
            if name.lower() == 'back':
                continue
            if name:
                attendance_list.append(name)
                print(f"{name} has been added to the attendance list.")
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
            print("Exiting the attendance recorder.")
            break

        else:
            print("Invalid option. Please choose a number between 1 and 4.")

# Run the attendance recorder
record_attendance()
