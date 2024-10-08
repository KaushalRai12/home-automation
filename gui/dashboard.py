import customtkinter as ctk
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
        self.window.geometry("500x500")
        
        # Set up the appearance mode and color theme for the dashboard
        ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
        ctk.set_default_color_theme("blue")  # "blue", "dark-blue", "green"

        # Frame for the dashboard
        self.frame = ctk.CTkFrame(self.window)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        self.dashboard_label = ctk.CTkLabel(self.frame, text=f"Welcome, {logged_in_username}", font=ctk.CTkFont(size=20, weight="bold"))
        self.dashboard_label.pack(pady=12, padx=10)

        # Change Password Button
        self.change_password_button = ctk.CTkButton(self.frame, text="Change Password", command=self.change_password)
        self.change_password_button.pack(pady=12, padx=10)

        # Manage Devices Button
        self.manage_devices_button = ctk.CTkButton(self.frame, text="Manage Devices", command=self.manage_devices)
        self.manage_devices_button.pack(pady=12, padx=10)

        # Monitor Devices Button
        self.monitor_devices_button = ctk.CTkButton(self.frame, text="Monitor Devices", command=self.monitor_devices)
        self.monitor_devices_button.pack(pady=12, padx=10)

        # If the user is an admin, show Manage Users Button
        if self.is_admin:
            self.manage_users_button = ctk.CTkButton(self.frame, text="Manage Users", command=self.open_manage_users_screen)
            self.manage_users_button.pack(pady=12, padx=10)

    def change_password(self):
        new_window = ctk.CTkToplevel(self.window)
        ChangePasswordScreen(new_window, self.logged_in_username)

    def manage_devices(self):
        new_window = ctk.CTkToplevel(self.window)
        ManageDevicesScreen(new_window, self.logged_in_username)

    def monitor_devices(self):
        new_window = ctk.CTkToplevel(self.window)
        MonitorDevicesScreen(new_window, self.logged_in_username)

    def open_manage_users_screen(self):
        manage_users_window = ctk.CTkToplevel(self.window)
        manage_users_window.title("Manage Users")
        ManageUsersScreen(manage_users_window)

# Test the Dashboard screen
if __name__ == "__main__":
    root = ctk.CTk()  # Using CTk for the main window
    app = DashboardScreen(root, logged_in_username="AdminUser", is_admin=True)
    root.mainloop()
