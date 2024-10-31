import tkinter as tk
from tkinter import messagebox, simpledialog

class ThreePointShotsTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Three-Point Shots Tracker")
        self.root.configure(bg='lightgreen')  # Set background color to light green
        
        self.shots_made = 0
        self.shots_list = []

        # Create GUI elements
        self.label = tk.Label(root, text="Three-Point Shots Tracker", font=("Arial", 16), bg='lightgreen')
        self.label.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Three-Point Shot", command=self.add_shot, bg='green', fg='white')
        self.add_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Total Shots Made", command=self.view_total, bg='green', fg='white')
        self.view_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Shots to File", command=self.save_shots, bg='green', fg='white')
        self.save_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit, bg='green', fg='white')
        self.exit_button.pack(pady=5)

    def add_shot(self):
        # Increase the count of shots made
        self.shots_made += 1
        self.shots_list.append(self.shots_made)
        messagebox.showinfo("Success", f"Three-point shot added! Total shots made: {self.shots_made}")

    def view_total(self):
        messagebox.showinfo("Total Shots Made", f"Total three-point shots made: {self.shots_made}")

    def save_shots(self):
        with open('three_point_shots.txt', 'w') as file:
            for shot in self.shots_list:
                file.write(f"{shot}\n")
        messagebox.showinfo("Success", "Shots list has been saved to 'three_point_shots.txt'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ThreePointShotsTracker(root)
    root.mainloop()
