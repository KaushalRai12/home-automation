import tkinter as tk
from tkinter import messagebox
import psycopg2

# Function to fetch data from PostgreSQL
def fetch_data():
    try:
        # Connect to PostgreSQL database
    
        conn = psycopg2.connect(
            host="localhost",
            database="home_automation",
            user="home-automation-admins",
            password="mypassword"
        )


        cur = conn.cursor()

        # Execute a query (example: fetching device status)
        cur.execute("SELECT id, device_name, status FROM public.devices;")
        records = cur.fetchall()

        # Clear the previous results in the listbox
        result_list.delete(0, tk.END)

        # Insert the new records into the listbox
        for record in records:
            result_list.insert(tk.END, f"Device: {record[0]}, Status: {record[1]}")

        # Close the cursor and connection
        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error connecting to the database: {str(e)}")

# Create the main GUI window
root = tk.Tk()
root.title("Home Automation System")

# Create a button to fetch data
fetch_button = tk.Button(root, text="Fetch Device Status", command=fetch_data)
fetch_button.pack(pady=10)

# Create a listbox to display the fetched data
result_list = tk.Listbox(root, width=50, height=10)
result_list.pack(pady=10)

# Run the GUI event loop
root.mainloop()
