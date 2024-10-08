import customtkinter as ctk
import psycopg2
from tkinter import messagebox

class MonitorDevicesScreen:
    def __init__(self, root_window, logged_in_username):
        self.window = root_window
        self.logged_in_username = logged_in_username

        # Set up appearance mode and color theme
        ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

        self.window.title(f"Monitor Devices - Logged in as {logged_in_username}")
        self.window.geometry("900x500")  # Make the window large enough to show all columns

        # Frame to hold the content
        self.frame = ctk.CTkFrame(self.window)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Title Label
        self.title_label = ctk.CTkLabel(self.frame, text="Your Devices", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=12, padx=10)

        # Scrollable frame to show devices
        self.devices_frame = ctk.CTkScrollableFrame(self.frame, width=600, height=350)
        self.devices_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Connect to the database and fetch devices
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()

            # Retrieve all columns from devices table
            cur.execute("SELECT device_name, device_type, connection_type, battery_level, energy_usage, status FROM devices")
            devices = cur.fetchall()

            # Create header for the table
            self.create_table_header()

            # Display each device in the scrollable frame
            for device in devices:
                self.create_device_row(device)

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error retrieving devices: {str(e)}")

    def create_table_header(self):
        """ Creates a header row for the device table. """
        header_frame = ctk.CTkFrame(self.devices_frame)
        header_frame.pack(fill="x")

        headers = ["Device Name", "Device Type", "Connection Type", "Battery Level", "Energy Usage", "Status"]
        for header in headers:
            label = ctk.CTkLabel(header_frame, text=header, width=100, anchor="w", font=ctk.CTkFont(weight="bold"))
            label.pack(side="left", padx=10)

    def create_device_row(self, device):
        """ Creates a row for each device displaying all columns. """
        device_name, device_type, connection_type, battery_level, energy_usage, status = device

        # Create a row for each device
        device_frame = ctk.CTkFrame(self.devices_frame)
        device_frame.pack(fill="x", pady=5, padx=10)

        # Display each column value
        device_name_label = ctk.CTkLabel(device_frame, text=device_name, width=100)
        device_name_label.pack(side="left", padx=10)

        device_type_label = ctk.CTkLabel(device_frame, text=device_type, width=100)
        device_type_label.pack(side="left", padx=10)

        connection_type_label = ctk.CTkLabel(device_frame, text=connection_type, width=100)
        connection_type_label.pack(side="left", padx=10)

        battery_level_label = ctk.CTkLabel(device_frame, text=str(battery_level) if battery_level is not None else "N/A", width=100)
        battery_level_label.pack(side="left", padx=10)

        energy_usage_label = ctk.CTkLabel(device_frame, text=str(energy_usage), width=100)
        energy_usage_label.pack(side="left", padx=10)

        # Status label with color coding
        status_var = ctk.StringVar(value=status)
        status_label = ctk.CTkLabel(device_frame, textvariable=status_var, width=60)
        status_label.pack(side="left", padx=10)

        # Update background color based on initial status
        self.update_device_background(status_label, status)

        # Toggle button to change status (on/off)
        toggle_switch = ctk.CTkSwitch(device_frame, text="",
                                      command=lambda: self.toggle_device_status(device_name, status_var, status_label),
                                      variable=status_var, onvalue="on", offvalue="off")
        toggle_switch.pack(side="right", padx=10)

    def toggle_device_status(self, device_name, status_var, status_label):
        """ Toggles the device's status in the database and updates the UI. """
        new_status = status_var.get()
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()

            # Update the device status in the database
            cur.execute("UPDATE devices SET status = %s WHERE device_name = %s", (new_status, device_name))
            conn.commit()
            cur.close()
            conn.close()

            # Success message
            messagebox.showinfo("Success", f"{device_name} has been turned {new_status}")

            # Update background color based on status
            self.update_device_background(status_label, new_status)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating device status: {str(e)}")

    def update_device_background(self, status_label, status):
        """ Updates the background color of the status label based on the status. """
        if status == "on":
            status_label.configure(fg_color="green")
        else:
            status_label.configure(fg_color="red")
