import customtkinter as ctk
from tkinter import messagebox
import psycopg2

class ChangePasswordScreen:
    def __init__(self, root_window, logged_in_username):
        self.window = root_window
        self.logged_in_username = logged_in_username

        self.window.title(f"Change Password - Logged in as {logged_in_username}")
        self.window.geometry("400x400")
        
        # Setting a nice dark theme look
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

        self.frame = ctk.CTkFrame(self.window)
        self.frame.pack(pady=20, padx=40, fill="both", expand=True)

        self.old_password_label = ctk.CTkLabel(self.frame, text="Old Password")
        self.old_password_label.pack(pady=12, padx=10)
        self.old_password_entry = ctk.CTkEntry(self.frame, show="*")
        self.old_password_entry.pack(pady=12, padx=10)

        self.new_password_label = ctk.CTkLabel(self.frame, text="New Password")
        self.new_password_label.pack(pady=12, padx=10)
        self.new_password_entry = ctk.CTkEntry(self.frame, show="*")
        self.new_password_entry.pack(pady=12, padx=10)

        self.change_button = ctk.CTkButton(self.frame, text="Change Password", command=self.change_password)
        self.change_button.pack(pady=25, padx=10)

    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()

        try:
            conn = psycopg2.connect(
                host="localhost",
                database="home_automation",
                user="home-automation-admins",
                password="mypassword"
            )
            cur = conn.cursor()

            # Check if the old password is correct
            cur.execute("SELECT password FROM users WHERE username = %s AND password = %s",
                        (self.logged_in_username, old_password))
            result = cur.fetchone()

            if result:
                # Update the password
                cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, self.logged_in_username))
                conn.commit()
                messagebox.showinfo("Success", "Password changed successfully!")
            else:
                messagebox.showerror("Error", "Old password is incorrect")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating password: {str(e)}")

# Test run
if __name__ == "__main__":
    root = ctk.CTk()  # Using customtkinter instead of Tk
    ChangePasswordScreen(root, "test_user")
    root.mainloop()
