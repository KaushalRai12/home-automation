import tkinter as tk
from change_password import ChangePasswordScreen
from manage_devices import ManageDevicesScreen
from monitor_devices import MonitorDevicesScreen
from manage_user import ManageUsersScreen

class DashboardScreen:
    def __init__(self, root_window, logged_in_username, is_admin):
        self.window = root_window
        self.is_admin = is_admin
        self.logged_in_username = logged_in_username
        
        self.window.title(f"Dashboard - Logged in as {logged_in_username}")
        self.window.geometry("400x400")

        change_password_button = tk.Button(self.window, text="Change Password", command=self.change_password)
        change_password_button.pack()

        manage_devices_button = tk.Button(self.window, text="Manage Devices", command=self.manage_devices)
        manage_devices_button.pack()

        monitor_devices_button = tk.Button(self.window, text="Monitor Devices", command=self.monitor_devices)
        monitor_devices_button.pack()

        if self.is_admin:
            manage_users_button = tk.Button(self.window, text="Manage Users", command=self.open_manage_users_screen)
            manage_users_button.pack(pady=10)

    def change_password(self):
        new_window = tk.Toplevel(self.window)
        ChangePasswordScreen(new_window, self.logged_in_username)

    def manage_devices(self):
        new_window = tk.Toplevel(self.window)
        ManageDevicesScreen(new_window, self.logged_in_username)

    def monitor_devices(self):
        new_window = tk.Toplevel(self.window)
        MonitorDevicesScreen(new_window, self.logged_in_username)

    def open_manage_users_screen(self):
        # Corrected the reference from self.root to self.window
        manage_users_window = tk.Toplevel(self.window)
        manage_users_window.title("Manage Users")
        ManageUsersScreen(manage_users_window)
