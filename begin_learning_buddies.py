#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, session, url_for, request, jsonify
import sqlite3

app = Flask(__name__)

# Set the secret key for Flask session
app.secret_key = ']!B+M5`sO@8Hgl[m?2,>RMI}'

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
                    confirm_password TEXT NOT NULL UNIQUE,
                    age INTEGER,
                    gender TEXT,
                    dob DATE,
                    telephone VARCHAR,
                    level_of_education TEXT,
                    courses_enrolled TEXT,
                    about_me TEXT,
                    mentor TEXT,
                    notification TEXT,
                    calendar DATETIME)''')
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

        # After successful signup, redirect to the profile page
        session['email'] = email  # Set the user's email in the session
        return redirect('/profile')
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
                # After successful login, set the user's email in the session and redirect to the profile page
                session['email'] = email
                return redirect('/profile')
            else:
                return render_template('login.html', error='Incorrect password')
        else:
            return render_template('login.html', error='User not found')
    return render_template('login.html')

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    return render_template('courses.html')

@app.route('/profile', methods=['POST'])
def profile():
    if 'email' in session:
        user_email = session['email']  # Retrieve user's email from the session
    else:
        # Handle the case when the user is not logged in
        return redirect('/login')  # Redirect to the login page or handle it appropriately

    # Fetch user's existing information from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ?', (user_email,))
    user = cursor.fetchone()

    if user:
        # Extract data from the request
        profile_data = request.json

        # Update user's information in the database
        cursor.execute('''UPDATE users SET 
                          gender=?, dob=?, telephone=?, level_of_education=?,
                          courses_enrolled=?, about_me=?, mentor=?, notification=?, calendar=?,
                          examination_notice=?, marksheet=?, any_other_info=?
                          WHERE id=?''',
                       (profile_data.get('gender'), profile_data.get('dob'), profile_data.get('telephone'),
                        profile_data.get('level_of_education'), profile_data.get('courses_enrolled'),
                        profile_data.get('about_me'), profile_data.get('mentor'), profile_data.get('notification'),
                        profile_data.get('calendar'), profile_data.get('examination_notice'),
                        profile_data.get('marksheet'), profile_data.get('any_other_info'), user['id']))
        conn.commit()
        conn.close()

        # Return a success response
        return jsonify({'message': 'Profile updated successfully'}), 200
    else:
        # Return an error response if user is not found
        return jsonify({'error': 'User not found'}), 404
# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user's session
    session.pop('email', None)

    # Redirect to the login page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
