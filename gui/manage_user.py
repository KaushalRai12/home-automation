import customtkinter as ctk
from tkinter import messagebox
import psycopg2

class ManageUsersScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Users")
        self.root.geometry("400x400")
        
        # Set up appearance mode and color theme
        ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

        # Create Frame for manage users form
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        # Title Label
        self.title_label = ctk.CTkLabel(self.frame, text="Manage Users", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=12, padx=10)

        # Create User Form
        self.create_user_label = ctk.CTkLabel(self.frame, text="Create New User")
        self.create_user_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.username_entry.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)
        self.role_entry = ctk.CTkEntry(self.frame, placeholder_text="Role (admin/user)")
        self.role_entry.pack(pady=5)
        self.create_user_button = ctk.CTkButton(self.frame, text="Create User", command=self.create_user)
        self.create_user_button.pack(pady=10)

        # Update User Form
        self.update_user_label = ctk.CTkLabel(self.frame, text="Update User")
        self.update_user_label.pack(pady=10)
        self.existing_username_entry = ctk.CTkEntry(self.frame, placeholder_text="Existing Username")
        self.existing_username_entry.pack(pady=5)
        self.new_password_entry = ctk.CTkEntry(self.frame, placeholder_text="New Password", show="*")
        self.new_password_entry.pack(pady=5)
        self.update_user_button = ctk.CTkButton(self.frame, text="Update User", command=self.update_user)
        self.update_user_button.pack(pady=10)

        # Delete User Form
        self.delete_user_label = ctk.CTkLabel(self.frame, text="Delete User")
        self.delete_user_label.pack(pady=10)
        self.delete_username_entry = ctk.CTkEntry(self.frame, placeholder_text="Username to Delete")
        self.delete_username_entry.pack(pady=5)
        self.delete_user_button = ctk.CTkButton(self.frame, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack(pady=10)

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", f"User {username} created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user: {str(e)}")

    def update_user(self):
        username = self.existing_username_entry.get()
        new_password = self.new_password_entry.get()

        if not username or not new_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()
            cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", f"User {username} updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")

    def delete_user(self):
        username = self.delete_username_entry.get()

        if not username:
            messagebox.showerror("Error", "Username is required.")
            return

        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE username = %s", (username,))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", f"User {username} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {str(e)}")


if __name__ == "__main__":
    root = ctk.CTk()  # Use customtkinter root window
    app = ManageUsersScreen(root)
    root.mainloop()
