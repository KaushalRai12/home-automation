import tkinter as tk
from change_password import ChangePasswordScreen
from manage_devices import ManageDevicesScreen
from monitor_devices import MonitorDevicesScreen

class DashboardScreen:
    def __init__(self, root_window, logged_in_username):
        self.window = root_window
        self.logged_in_username = logged_in_username

        self.window.title(f"Dashboard - Logged in as {logged_in_username}")
        self.window.geometry("400x400")

        change_password_button = tk.Button(self.window, text="Change Password", command=self.change_password)
        change_password_button.pack()

        manage_devices_button = tk.Button(self.window, text="Manage Devices", command=self.manage_devices)
        manage_devices_button.pack()

        monitor_devices_button = tk.Button(self.window, text="Monitor Devices", command=self.monitor_devices)
        monitor_devices_button.pack()

    def change_password(self):
        new_window = tk.Toplevel(self.window)
        ChangePasswordScreen(new_window, self.logged_in_username)

    def manage_devices(self):
        new_window = tk.Toplevel(self.window)
        ManageDevicesScreen(new_window, self.logged_in_username)

    def monitor_devices(self):
        new_window = tk.Toplevel(self.window)
        MonitorDevicesScreen(new_window, self.logged_in_username)
