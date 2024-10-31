import tkinter as tk
from tkinter import messagebox, simpledialog

class AttendanceRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Recorder")
        self.root.configure(bg='lightgreen') #background colour
        
        self.attendance_list = self.load_attendance()
        self.admin_passwords = ["admin123", "owandho254", "123456789"]

        # Create GUI elements
        self.label = tk.Label(root, text="Attendance Recorder", font=("Arial", 16))
        self.label.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Student", command=self.add_student)
        self.add_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Attendance List", command=self.view_attendance)
        self.view_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Attendance to File", command=self.save_attendance)
        self.save_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Student (Admin Only)", command=self.delete_student)
        self.delete_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=5)

    def load_attendance(self):
        try:
            with open('attendance_list.txt', 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def add_student(self):
        name = simpledialog.askstring("Add Student", "Enter the student's name:")
        if name:
            self.attendance_list.append(name)
            messagebox.showinfo("Success", f"{name} has been added to the attendance list.")

    def view_attendance(self):
        if self.attendance_list:
            attendance_str = "\n".join(f"{index + 1}. {student}" for index, student in enumerate(self.attendance_list))
            messagebox.showinfo("Attendance List", attendance_str)
        else:
            messagebox.showinfo("Attendance List", "No students have attended yet.")

    def save_attendance(self):
        with open('attendance_list.txt', 'w') as file:
            for student in self.attendance_list:
                file.write(f"{student}\n")
        messagebox.showinfo("Success", "Attendance list has been saved.")

    def delete_student(self):
        password = simpledialog.askstring("Admin Password", "Enter your admin password:")
        if password in self.admin_passwords:
            name = simpledialog.askstring("Delete Student", "Enter the student's name to delete:")
            if name in self.attendance_list:
                self.attendance_list.remove(name)
                messagebox.showinfo("Success", f"{name} has been deleted from the attendance list.")
            else:
                messagebox.showwarning("Not Found", f"{name} is not in the attendance list.")
        else:
            messagebox.showwarning("Access Denied", "Invalid admin password.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceRecorder(root)
    root.mainloop()
