#!/usr/bin/python3

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('learning-buddies.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    new_password TEXT NOT NULL UNIQUE,
                    confirm_password TEXT NOT NULL UNIQUE)''')
    conn.commit()
    conn.close()

create_table()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        conn = get_db_connection()
        conn.execute('INSERT INTO users (first_name, last_name, email, new_password, confirm_password) VALUES (?, ?, ?, ?, ?)',
                     (first_name, last_name, email, new_password, confirm_password))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Retrieve user's data from the database based on the provided email
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT email, new_password FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Check if the provided password matches the stored password
            if password == user['new_password']:
                return redirect('/')  # Redirect to home page upon successful login
            else:
                return render_template('login.html', error='Incorrect password')
        else:
            return render_template('login.html', error='User not found')
    return render_template('login.html')

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    return render_template('courses.html')

if __name__ == '__main__':
    app.run(debug=True)
