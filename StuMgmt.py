import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


# Initialize the SQLite Database
def initialize_db():
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Gender TEXT NOT NULL,
            Course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Add a new student to the database
def add_student():
    name = name_var.get()
    age = age_var.get()
    gender = gender_var.get()
    course = course_var.get()

    if not name or not age or not gender or not course:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Students (Name, Age, Gender, Course)
        VALUES (?, ?, ?, ?)
    ''', (name, age, gender, course))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student added successfully!")
    fetch_students()
    clear_form()


# Fetch all students and display in the treeview
def fetch_students():
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students')
    rows = cursor.fetchall()
    conn.close()

    for row in student_tree.get_children():
        student_tree.delete(row)

    for row in rows:
        student_tree.insert("", END, values=row)


# Clear the form inputs
def clear_form():
    name_var.set("")
    age_var.set("")
    gender_var.set("")
    course_var.set("")


# Delete a selected student
def delete_student():
    selected_item = student_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No student selected!")
        return

    student_id = student_tree.item(selected_item)["values"][0]
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Students WHERE ID = ?', (student_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student deleted successfully!")
    fetch_students()


# Update a selected student
def update_student():
    selected_item = student_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No student selected!")
        return

    student_id = student_tree.item(selected_item)["values"][0]
    name = name_var.get()
    age = age_var.get()
    gender = gender_var.get()
    course = course_var.get()

    if not name or not age or not gender or not course:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Students
        SET Name = ?, Age = ?, Gender = ?, Course = ?
        WHERE ID = ?
    ''', (name, age, gender, course, student_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student updated successfully!")
    fetch_students()
    clear_form()


# Populate the form with selected student data
def populate_form(event):
    selected_item = student_tree.selection()
    if selected_item:
        row = student_tree.item(selected_item)["values"]
        name_var.set(row[1])
        age_var.set(row[2])
        gender_var.set(row[3])
        course_var.set(row[4])


# Initialize the main window
root = Tk()
root.title("Student Management System")
root.geometry("800x500")

# Form Variables
name_var = StringVar()
age_var = StringVar()
gender_var = StringVar()
course_var = StringVar()

# Form Frame
form_frame = Frame(root, padx=10, pady=10)
form_frame.pack(side=TOP, fill=X)

Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
Entry(form_frame, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5, sticky=W)

Label(form_frame, text="Age:").grid(row=0, column=2, padx=5, pady=5, sticky=W)
Entry(form_frame, textvariable=age_var).grid(row=0, column=3, padx=5, pady=5, sticky=W)

Label(form_frame, text="Gender:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
gender_dropdown = ttk.Combobox(form_frame, textvariable=gender_var, values=("Male", "Female"))
gender_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky=W)

Label(form_frame, text="Course:").grid(row=1, column=2, padx=5, pady=5, sticky=W)
Entry(form_frame, textvariable=course_var).grid(row=1, column=3, padx=5, pady=5, sticky=W)

Button(form_frame, text="Add", command=add_student).grid(row=2, column=0, padx=5, pady=10)
Button(form_frame, text="Update", command=update_student).grid(row=2, column=1, padx=5, pady=10)
Button(form_frame, text="Delete", command=delete_student).grid(row=2, column=2, padx=5, pady=10)
Button(form_frame, text="Clear", command=clear_form).grid(row=2, column=3, padx=5, pady=10)

# Treeview Frame
tree_frame = Frame(root, padx=10, pady=10)
tree_frame.pack(fill=BOTH, expand=True)

# Treeview for displaying student data
columns = ("ID", "Name", "Age", "Gender", "Course")
student_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    student_tree.heading(col, text=col)
    student_tree.column(col, width=100)

student_tree.pack(fill=BOTH, expand=True)
student_tree.bind("<<TreeviewSelect>>", populate_form)

# Initialize Database and Load Data
initialize_db()
fetch_students()

root.mainloop()
