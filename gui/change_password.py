import tkinter as tk
from tkinter import messagebox
import psycopg2

class ChangePasswordScreen:
    def __init__(self, root_window, logged_in_username):
        self.window = root_window
        self.logged_in_username = logged_in_username

        self.window.title(f"Change Password - Logged in as {logged_in_username}")
        self.window.geometry("300x200")

        self.old_password_label = tk.Label(self.window, text="Old Password")
        self.old_password_label.pack()
        self.old_password_entry = tk.Entry(self.window, show="*")
        self.old_password_entry.pack()

        self.new_password_label = tk.Label(self.window, text="New Password")
        self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self.window, show="*")
        self.new_password_entry.pack()

        self.change_button = tk.Button(self.window, text="Change Password", command=self.change_password)
        self.change_button.pack()

    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()

        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()

            # Check if the old password is correct
            cur.execute("SELECT password FROM users WHERE username = %s AND password = %s",
                        (self.logged_in_username, old_password))
            result = cur.fetchone()

            if result:
                # Update the password
                cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, self.logged_in_username))
                conn.commit()
                messagebox.showinfo("Success", "Password changed successfully!")
            else:
                messagebox.showerror("Error", "Old password is incorrect")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating password: {str(e)}")
