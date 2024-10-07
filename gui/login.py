import tkinter as tk
from tkinter import messagebox
import psycopg2

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")

        # Username and password labels and text entry fields
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        self.login_button = tk.Button(root, text="Login", command=self.authenticate)
        self.login_button.pack(pady=20)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Connect to PostgreSQL to verify login credentials
        try:
            conn = psycopg2.connect(
               host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            messagebox.showinfo("Login Successful", "Welcome!")
            self.root.destroy()  # Close the login window
            self.open_dashboard()  # Open dashboard window

        except psycopg2.OperationalError as e:
            messagebox.showerror("Login Failed", f"Error: {str(e)}")
    
    def open_dashboard(self):
        # Open dashboard screen after successful login
        dashboard = tk.Tk()
        DashboardScreen(dashboard)
        dashboard.mainloop()

class DashboardScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("400x300")

        # Add buttons for each function
        self.change_password_button = tk.Button(root, text="Change Password", command=self.change_password)
        self.change_password_button.pack(pady=10)

        self.device_management_button = tk.Button(root, text="Manage Devices", command=self.manage_devices)
        self.device_management_button.pack(pady=10)

        self.monitor_device_button = tk.Button(root, text="Monitor Devices", command=self.monitor_devices)
        self.monitor_device_button.pack(pady=10)

    def change_password(self):
        messagebox.showinfo("Change Password", "Function to change password.")

    def manage_devices(self):
        messagebox.showinfo("Manage Devices", "Function to manage devices.")

    def monitor_devices(self):
        messagebox.showinfo("Monitor Devices", "Function to monitor device status.")

if __name__ == "__main__":
    root = tk.Tk()
    login = LoginScreen(root)
    root.mainloop()
