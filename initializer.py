def assign_user_ids(names):
    # Sort names alphabetically
    sorted_names = sorted(names)
    
    # Create a dictionary to store user IDs with initials and numbers
    user_ids = {}
    counts = {} # Track duplicate files 
    
    for i, name in enumerate(sorted_names, start=1):
        # Split name and create initials
        initials = ''.join([part[0].upper() for part in name.split()])
        
        #Handle duplicates
        if initials not in counts:
            counts[initials] = 0
        counts[initials] += 1

        # Combine initials with user number
        user_id = f"{initials}{i:03}"  # Pads the number with leading zeros (e.g., 001, 002)
        
        #If duplicate to append to count
        if counts [initials] > 1:
            user_id = f"{initials}{counts[initials]:03}"
        
        # Store in dictionary
        user_ids[name] = user_id
    
    return user_ids

# Example usage
names = ["Alice Johnson", "Bob Smith", "Charlie Brown", "Alice Smith"]
user_ids = assign_user_ids(names)

for name, user_id in user_ids.items():
    print(f"Name: {name}, User ID: {user_id}")
