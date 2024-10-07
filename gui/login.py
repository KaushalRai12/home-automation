import tkinter as tk
from tkinter import messagebox
import psycopg2
from dashboard import DashboardScreen

class LoginScreen:
    def __init__(self, root_window):
        self.window = root_window
        self.window.title("Login")
        self.window.geometry("300x200")

        self.username_label = tk.Label(self.window, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.window, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.window, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check credentials in the PostgreSQL database
        try:
            conn = psycopg2.connect(
                 host="localhost",
                 database="home_automation",
                 user="home-automation-admins",
                 password="mypassword"
            )
            cur = conn.cursor()

            # Query to check if the user exists with the given username and password
            cur.execute("SELECT username FROM users WHERE username = %s AND password = %s", (username, password))
            result = cur.fetchone()

            if result:
                # Successful login
                self.window.destroy()  # Close the login window
                root = tk.Tk()
                DashboardScreen(root, username)  # Pass the username to the dashboard
                root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid credentials")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()
