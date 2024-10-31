from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Load existing attendance from file if available
try:
    with open('attendance_list.txt', 'r') as file:
        attendance_list = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    attendance_list = []  # Start with an empty list

admin_passwords = ["admin123", "owandho254", "123456789"]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'add_student' in request.form:
            name = request.form['name']
            if name and name not in attendance_list:
                attendance_list.append(name)
                flash(f"{name} has been added to the attendance list.")
            elif name in attendance_list:
                flash(f"{name} is already in the attendance list.")
            else:
                flash("Name cannot be empty.")
                #delete student
        elif 'delete_student' in request.form:
            password = request.form['admin_password']
            name = request.form['student_to_delete']
            if password in admin_passwords:
                if name in attendance_list:
                    attendance_list.remove(name)
                    flash(f"{name} has been deleted from the attendance list.")
                else:
                    flash(f"{name} is not in the attendance list.")
            else:
                flash("Invalid admin password. Access denied.")

        return redirect(url_for('home'))

    return render_template('index.html', attendance_list=attendance_list)

@app.route('/save', methods=['POST'])
def save():
    with open('attendance_list.txt', 'w') as file:
        for student in attendance_list:
            file.write(f"{student}\n")
    flash("Attendance list has been saved.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
