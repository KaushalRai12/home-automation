from flask import Flask, render_template, request, redirect, url_for, session ,flash

import psycopg2

app = Flask(__name__)
app.secret_key = 'yoursecretkey'

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="home_automation",
        user="home-automation-admins",
        password="mypassword"
    )
    return conn

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username, role FROM users WHERE username = %s AND password = %s", (username, password))
        result = cur.fetchone()

        if result:
            session['logged_in'] = True
            session['username'] = result[0]
            session['role'] = result[1]
            return redirect(url_for('dashboard'))

        return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        username = session['username']
        is_admin = session['role'] == 'admin'
        return render_template('dashboard.html', username=username, is_admin=is_admin)
    else:
        return redirect(url_for('login'))

# Change Password route
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        username = session.get('username')

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if current password matches
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

        if result and result[0] == current_password:
            # Update the password
            cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
            conn.commit()
            cur.close()
            conn.close()

            # Redirect with success message to dashboard
            return redirect(url_for('dashboard'))
        else:
            return render_template('change_password.html', error="Current password is incorrect")

    return render_template('change_password.html')


# Manage Devices route
@app.route('/manage_devices', methods=['GET', 'POST'])
def manage_devices():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        # Adding a new device
        device_name = request.form['device_name']
        device_type = request.form['device_type']
        connection_type = request.form['connection_type']
        
        cur.execute("INSERT INTO devices (device_name, device_type, connection_type, status, provisioned) VALUES (%s, %s, %s, 'off', FALSE)", 
                    (device_name, device_type, connection_type))
        conn.commit()
        flash("Device added successfully", "success")
        return redirect(url_for('manage_devices'))

    # Fetch devices from the database
    cur.execute("SELECT device_name,device_type,connection_type,battery_level,energy_usage, status, provisioned FROM devices")
    devices = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('manage_devices.html', devices=devices)

# Toggle Device Status
@app.route('/toggle_device_status/<device_name>', methods=['POST'])
def toggle_device_status(device_name):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    new_status = request.form['status']
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE devices SET status = %s WHERE device_name = %s", (new_status, device_name))
    conn.commit()
    cur.close()
    conn.close()

    flash(f"Device '{device_name}' turned {new_status}", "success")
    return redirect(url_for('manage_devices'))

# Add Device route
@app.route('/add_device', methods=['POST'])
def add_device():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    # Get the device details from the form
    device_name = request.form['device_name']
    device_type = request.form['device_type']
    connection_type = request.form['connection_type']

    if device_name and device_type and connection_type:
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert the new device into the database
        cur.execute("INSERT INTO devices (device_name, device_type, connection_type, status, provisioned) VALUES (%s, %s, %s, 'off', FALSE)", 
                    (device_name, device_type, connection_type))
        conn.commit()
        cur.close()
        conn.close()

        flash(f"Device '{device_name}' added successfully", "success")
    else:
        flash("All fields are required to add a device", "error")

    return redirect(url_for('manage_devices'))

# Remove Device
@app.route('/remove_device/<device_name>', methods=['POST'])
def remove_device(device_name):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM devices WHERE device_name = %s", (device_name,))
    conn.commit()
    cur.close()
    conn.close()

    flash(f"Device '{device_name}' removed successfully", "success")
    return redirect(url_for('manage_devices'))

# Monitor Devices route
@app.route('/monitor_devices', methods=['GET'])
def monitor_devices():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    # Logic to fetch device monitoring data can be added here
    return render_template('monitor_devices.html')

# Manage Users route
@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if 'logged_in' not in session or session['role'] != 'admin':
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch all users from the database
    cur.execute("SELECT username, role FROM users")
    users = cur.fetchall()

    if request.method == 'POST':
        # Handle creating or updating users
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        conn.commit()

    cur.close()
    conn.close()

    return render_template('manage_users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
