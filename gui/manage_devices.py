import tkinter as tk
import psycopg2

class ManageDevicesScreen:
    def __init__(self, root_window, logged_in_username):
        self.window = root_window
        self.logged_in_username = logged_in_username

        self.window.title(f"Manage Devices - Logged in as {logged_in_username}")
        self.window.geometry("400x300")

        tk.Label(self.window, text="Your Devices").pack()

        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()

            # Retrieve devices owned by the logged-in user
            cur.execute("SELECT device_name FROM devices")
            devices = cur.fetchall()

            for device in devices:
                tk.Label(self.window, text=device[0]).pack()

            cur.close()
            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Database Error", f"Error retrieving devices: {str(e)}")
