def basketball_score_tracker():
    total_score = 0
    total_shots = 0

    while True:
        print("\nBasketball Score Tracker")
        print("------------------------")
        print("1. Add Two-Point Shot")
        print("2. Add Three-Point Shot")
        print("3. View Total Score")
        print("4. View Total Shots Made")
        print("5. Bonus points")
        print("6. Exit")
        
        choice = input("Choose an option (1-6): ")
        if choice == '1':
            total_score += 2
            total_shots += 1
            print(f"Two-point shot made! Score is {total_score}.")
        
        elif choice == '2':
            total_score += 3
            total_shots += 1
            print(f"Th
                  ree-point shot made!. Total score is{total_score}")
        
        elif choice == '3':
            print(f"Total score: {total_score} points")
        
        elif choice == '4':
            print(f"Total shots made: {total_shots}")

        elif choice == '5':
            if total_score > 15:
                total_score += 1
                print(f"Score is {total_score}")
        
        elif choice == '6':
            confirm_exit = input("Are you sure you want to exit(yes/no): ")
            if confirm_exit == 'yes':
                print("Exiting the score tracker.")
                break
            else:
                continue
        
        else:
           print("Invalid option. Please choose a number between 1 and 6.")

basketball_score_tracker()
