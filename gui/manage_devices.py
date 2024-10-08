import customtkinter as ctk
import psycopg2
from tkinter import messagebox

class ManageDevicesScreen:
    def __init__(self, root_window, logged_in_username):
        self.window = root_window
        self.logged_in_username = logged_in_username

        # Set up appearance mode and color theme
        ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

        self.window.title(f"Manage Devices - Logged in as {logged_in_username}")
        self.window.geometry("1000x600")  # Adjusted for more space to include the 'Provisioned' column

        # Frame to hold the content
        self.frame = ctk.CTkFrame(self.window)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Title Label
        self.title_label = ctk.CTkLabel(self.frame, text="Your Devices", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=12, padx=10)

        # Scrollable frame to show devices
        self.devices_frame = ctk.CTkScrollableFrame(self.frame, width=600, height=350)
        self.devices_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Button to add and remove devices
        self.add_device_button = ctk.CTkButton(self.frame, text="Add Device", command=self.add_device)
        self.add_device_button.pack(pady=10)

        self.remove_device_button = ctk.CTkButton(self.frame, text="Remove Device", command=self.remove_device)
        self.remove_device_button.pack(pady=10)

        # Connect to the database and fetch devices
        self.load_devices()

    def load_devices(self):
        """ Fetch devices and display them in the table. """
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()

            # Retrieve all columns from devices table including 'provisioned'
            cur.execute("SELECT device_name, device_type, connection_type, battery_level, energy_usage, status, provisioned FROM devices")
            devices = cur.fetchall()

            # Clear previous device entries
            for widget in self.devices_frame.winfo_children():
                widget.destroy()

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

        headers = ["Device Name", "Device Type", "Connection Type", "Battery Level", "Energy Usage", "Status", "Provisioned"]
        for header in headers:
            label = ctk.CTkLabel(header_frame, text=header, width=120, anchor="w", font=ctk.CTkFont(weight="bold"))
            label.pack(side="left", padx=10)

    def create_device_row(self, device):
        """ Creates a row for each device displaying all columns. """
        device_name, device_type, connection_type, battery_level, energy_usage, status, provisioned = device

        # Create a row for each device
        device_frame = ctk.CTkFrame(self.devices_frame)
        device_frame.pack(fill="x", pady=5, padx=10)

        # Display each column value
        device_name_label = ctk.CTkLabel(device_frame, text=device_name, width=120)
        device_name_label.pack(side="left", padx=10)

        device_type_label = ctk.CTkLabel(device_frame, text=device_type, width=120)
        device_type_label.pack(side="left", padx=10)

        connection_type_label = ctk.CTkLabel(device_frame, text=connection_type, width=120)
        connection_type_label.pack(side="left", padx=10)

        battery_level_label = ctk.CTkLabel(device_frame, text=str(battery_level) if battery_level is not None else "N/A", width=120)
        battery_level_label.pack(side="left", padx=10)

        energy_usage_label = ctk.CTkLabel(device_frame, text=str(energy_usage), width=120)
        energy_usage_label.pack(side="left", padx=10)

        # Status label with color coding
        status_var = ctk.StringVar(value=status)
        status_label = ctk.CTkLabel(device_frame, textvariable=status_var, width=60)
        status_label.pack(side="left", padx=10)

        # Provisioned status
        provisioned_label = ctk.CTkLabel(device_frame, text="Yes" if provisioned else "No", fg_color="green" if provisioned else "red", width=100)
        provisioned_label.pack(side="left", padx=10)

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

    def add_device(self):
        """ Opens a form to add a new device to the system. """
        add_device_window = ctk.CTkToplevel(self.window)
        add_device_window.title("Add Device")
        add_device_window.geometry("400x300")

        # Fields for device information
        ctk.CTkLabel(add_device_window, text="Device Name").pack(pady=10)
        device_name_entry = ctk.CTkEntry(add_device_window)
        device_name_entry.pack(pady=5)

        ctk.CTkLabel(add_device_window, text="Device Type").pack(pady=10)
        device_type_entry = ctk.CTkEntry(add_device_window)
        device_type_entry.pack(pady=5)

        ctk.CTkLabel(add_device_window, text="Connection Type").pack(pady=10)
        connection_type_entry = ctk.CTkEntry(add_device_window)
        connection_type_entry.pack(pady=5)

        # Button to save device
        def save_device():
            device_name = device_name_entry.get()
            device_type = device_type_entry.get()
            connection_type = connection_type_entry.get()

            if device_name and device_type and connection_type:
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        database="home_automation",
                        user="home-automation-admins",
                        password="mypassword"
                    )
                    cur = conn.cursor()

                    cur.execute("INSERT INTO devices (device_name, device_type, connection_type, status, provisioned) VALUES (%s, %s, %s, 'off', FALSE)",
                                (device_name, device_type, connection_type))
                    conn.commit()
                    cur.close()
                    conn.close()

                    messagebox.showinfo("Success", f"Device '{device_name}' added successfully.")
                    add_device_window.destroy()

                    # Reload devices
                    self.load_devices()

                except Exception as e:
                    messagebox.showerror("Database Error", f"Error adding device: {str(e)}")
            else:
                messagebox.showerror("Error", "All fields are required.")

        ctk.CTkButton(add_device_window, text="Add Device", command=save_device).pack(pady=10)

    def remove_device(self):
        """ Opens a form to remove an existing device. """
        remove_device_window = ctk.CTkToplevel(self.window)
        remove_device_window.title("Remove Device")
        remove_device_window.geometry("400x200")

        # Device name to remove
        ctk.CTkLabel(remove_device_window, text="Device Name").pack(pady=10)
        device_name_entry = ctk.CTkEntry(remove_device_window)
        device_name_entry.pack(pady=5)

        # Button to remove device
        def delete_device():
            device_name = device_name_entry.get()

            if device_name:
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        database="home_automation",
                        user="home-automation-admins",
                        password="mypassword"
                    )
                    cur = conn.cursor()

                    cur.execute("DELETE FROM devices WHERE device_name = %s", (device_name,))
                    conn.commit()
                    cur.close()
                    conn.close()

                    messagebox.showinfo("Success", f"Device '{device_name}' removed successfully.")
                    remove_device_window.destroy()

                    # Reload devices
                    self.load_devices()

                except Exception as e:
                    messagebox.showerror("Database Error", f"Error removing device: {str(e)}")
            else:
                messagebox.showerror("Error", "Device name is required.")

        ctk.CTkButton(remove_device_window, text="Remove Device", command=delete_device).pack(pady=10)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ManageDevicesScreen(root, "admin_user")
    root.mainloop()
