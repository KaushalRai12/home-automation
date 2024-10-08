import customtkinter as ctk
import psycopg2
from tkinter import messagebox
from dashboard import DashboardScreen

# Set the appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class LoginScreen:
    def __init__(self, root_window):
        self.window = root_window
        self.window.title("Login")
        self.window.geometry("400x400")
        self.window.configure(padx=30, pady=30)

        # Title Label
        self.title_label = ctk.CTkLabel(self.window, text="Login", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # Username Entry
        self.username_label = ctk.CTkLabel(self.window, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.window, width=250)
        self.username_entry.pack(pady=5)

        # Password Entry
        self.password_label = ctk.CTkLabel(self.window, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.window, show="*", width=250)
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = ctk.CTkButton(self.window, text="Login", command=self.login, width=200)
        self.login_button.pack(pady=20)

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
            cur.execute("SELECT username, role FROM users WHERE username = %s AND password = %s", (username, password))
            result = cur.fetchone()

            if result:
                # Successful login
                role = result[1]
                is_admin = role == 'admin'  # Set the flag based on role
                self.window.destroy()  # Close the login window
                root = ctk.CTk()
                DashboardScreen(root, username, is_admin)  # Pass the username to the dashboard
                root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid credentials")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {str(e)}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginScreen(root)
    root.mainloop()
