import tkinter as tk
import psycopg2

class MonitorDevicesScreen:
    def __init__(self, root_window, logged_in_username):
        self.window = root_window
        self.logged_in_username = logged_in_username

        self.window.title(f"Monitor Devices - Logged in as {logged_in_username}")
        self.window.geometry("400x300")

        tk.Label(self.window, text="Monitoring Devices").pack()

        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()

            # Retrieve devices and their statuses
            cur.execute("SELECT device_name, status FROM devices")
            devices = cur.fetchall()

            for device in devices:
                tk.Label(self.window, text=f"{device[0]} - {device[1]}").pack()

            cur.close()
            conn.close()

        except Exception as e:
            tk.messagebox.showerror("Database Error", f"Error monitoring devices: {str(e)}")
