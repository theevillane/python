import tkinter as tk
from tkinter import messagebox

class BasketballScoreTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Basketball Score Tracker")
        self.root.configure(bg='lightblue')  # Set background color

        self.total_score = 0
        self.total_shots = 0

        # Create GUI elements
        self.label = tk.Label(root, text="Basketball Score Tracker", font=("Arial", 16), bg='lightblue')
        self.label.pack(pady=10)

        self.score_label = tk.Label(root, text=f"Total Score: {self.total_score} points", font=("Arial", 14), bg='lightblue')
        self.score_label.pack(pady=10)

        self.two_point_button = tk.Button(root, text="Add Two-Point Shot", command=self.add_two_point, bg='blue', fg='white')
        self.two_point_button.pack(pady=5)

        self.three_point_button = tk.Button(root, text="Add Three-Point Shot", command=self.add_three_point, bg='blue', fg='white')
        self.three_point_button.pack(pady=5)

        self.view_shots_button = tk.Button(root, text="View Total Shots Made", command=self.view_total_shots, bg='blue', fg='white')
        self.view_shots_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit, bg='blue', fg='white')
        self.exit_button.pack(pady=5)

    def add_two_point(self):
        self.total_score += 2
        self.total_shots += 1
        self.update_score_label()
        messagebox.showinfo("Success", "Added a two-point shot.")

    def add_three_point(self):
        self.total_score += 3
        self.total_shots += 1
        self.update_score_label()
        messagebox.showinfo("Success", "Added a three-point shot.")

    def update_score_label(self):
        self.score_label.config(text=f"Total Score: {self.total_score} points")

    def view_total_shots(self):
        messagebox.showinfo("Total Shots Made", f"Total shots made: {self.total_shots}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BasketballScoreTracker(root)
    root.mainloop()
