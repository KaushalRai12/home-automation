from flask import Flask, render_template, request, redirect, url_for, session
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

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        # Handle password change logic
        pass
    return render_template('change_password.html')

@app.route('/manage_devices', methods=['GET'])
def manage_devices():
    return render_template('manage_devices.html')

@app.route('/monitor_devices', methods=['GET'])
def monitor_devices():
    return render_template('monitor_devices.html')

@app.route('/manage_users', methods=['GET'])
def manage_users():
    return render_template('manage_users.html')


if __name__ == '__main__':
    app.run(debug=True)
