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
      #choices 
        if choice == '1':
            total_score += 2
            total_shots += 1
            print("Added a two-point shot.")
        
        elif choice == '2':
            total_score += 3
            total_shots += 1
            print("Added a three-point shot.")
        
        elif choice == '3':
            print(f"Total score: {total_score} points")
        
        elif choice == '4':
            print(f"Total shots made: {total_shots}")

        elif choice == '5':
            if shot > 3:
                print("Added ! point")
        
        elif choice == '6':
            print("Exiting the score tracker.")
            break
        
        else:
            print("Invalid option. Please choose a number between 1 and 5.")

# Run
basketball_score_tracker()
