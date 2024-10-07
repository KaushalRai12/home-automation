from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="home_automation",
        user="home-automation-admins",
        password="mypassword"
    )
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, device_name, status FROM public.devices;')
    db_version = cur.fetchall()
    cur.close()
    conn.close()
    return f"Connected to PostgreSQL - {db_version}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
