from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="home_automation",
        user="home-automation-admins",
        password="mypassword"
    )
    return conn

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT username, role FROM users WHERE username = %s AND password = %s", (username, password))
        result = cur.fetchone()

        if result:
            role = result[1]
            return f"Logged in as {username}, Role: {role}"
        else:
            error = 'Invalid username or password'
        
        cur.close()
        conn.close()

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
