import tkinter as tk
from tkinter import messagebox
import psycopg2

class ManageUsersScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Users")

        # Create User Form
        tk.Label(root, text="Create New User").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(root, text="Username").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(root, text="Password").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(root, text="Role (admin/user)").grid(row=3, column=0, padx=10, pady=5)

        self.username_entry = tk.Entry(root)
        self.password_entry = tk.Entry(root, show="*")
        self.role_entry = tk.Entry(root)

        self.username_entry.grid(row=1, column=1)
        self.password_entry.grid(row=2, column=1)
        self.role_entry.grid(row=3, column=1)

        tk.Button(root, text="Create User", command=self.create_user).grid(row=4, column=1, pady=10)

        # Update User Form
        tk.Label(root, text="Update User").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(root, text="Existing Username").grid(row=6, column=0, padx=10, pady=5)
        tk.Label(root, text="New Password").grid(row=7, column=0, padx=10, pady=5)

        self.existing_username_entry = tk.Entry(root)
        self.new_password_entry = tk.Entry(root, show="*")

        self.existing_username_entry.grid(row=6, column=1)
        self.new_password_entry.grid(row=7, column=1)

        tk.Button(root, text="Update User", command=self.update_user).grid(row=8, column=1, pady=10)

        # Delete User Form
        tk.Label(root, text="Delete User").grid(row=9, column=0, padx=10, pady=10)
        tk.Label(root, text="Username to Delete").grid(row=10, column=0, padx=10, pady=5)

        self.delete_username_entry = tk.Entry(root)
        self.delete_username_entry.grid(row=10, column=1)

        tk.Button(root, text="Delete User", command=self.delete_user).grid(row=11, column=1, pady=10)

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            conn = psycopg2.connect(
            host="localhost",
            database="home_automation",
            user="home-automation-admins",
            password="mypassword"
        )
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", f"User {username} created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user: {str(e)}")

    def update_user(self):
        username = self.existing_username_entry.get()
        new_password = self.new_password_entry.get()

        if not username or not new_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            conn = psycopg2.connect(
            host="localhost",
            database="home_automation",
            user="home-automation-admins",
            password="mypassword"
        )
            cur = conn.cursor()
            cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", f"User {username} updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")

    def delete_user(self):
        username = self.delete_username_entry.get()

        if not username:
            messagebox.showerror("Error", "Username is required.")
            return

        try:
            conn = psycopg2.connect(
            host="localhost",
            database="home_automation",
            user="home-automation-admins",
            password="mypassword"
        )
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE username = %s", (username,))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", f"User {username} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
