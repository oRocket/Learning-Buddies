#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = ']!B+M5`sO@8Hgl[m?2,>RMI}'

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Dummy user class for demonstration (replace with your actual User model)
class User(UserMixin):
    def _init_(self):
        pass


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
       user = User()
       user.id = user_data['id']
       user.email = user_data['email']
       user.first_name = user_data['first_name']
       user.last_name = user_data['last_name']
       return user
    else:
        return None

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
                    password TEXT NOT NULL,
                    confirm_password TEXT NOT NULL,
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

# Update the signup route to hash passwords before storing them
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        confirm_password = request.form['confirm_password']

        conn = get_db_connection()
        conn.execute('INSERT INTO users (first_name, last_name, email, password, confirm_password) VALUES (?, ?, ?, ?, ?)',
                     (first_name, last_name, email, password, confirm_password))
        conn.commit()
        conn.close()

        # After successful signup, redirect to the profile page
        session['email'] = email  # Set the user's email in the session
        return redirect('/profile')
    return render_template('signup.html')


# Update the login route to verify passwords using bcrypt
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve user's data from the database based on the provided email
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user:
            # Check if the provided password matches the hashed password in the database
            if bcrypt.check_password_hash(user['password'], password):
                # Authentication successful, store user email in session and redirect to profile page
                session['email'] = email
                return redirect('/profile')
            else:
                # Password does not match, render login page with error message
                return render_template('login.html', error='Invalid email or password')
        else:
            # User not found, render login page with error message
            return render_template('login.html', error='User not found')
    return render_template('login.html')


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    return render_template('courses.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if 'email' in session:
        user_email = session['email']  # Retrieve user's email from the session
    else:
        # Handle the case when the user is not logged in
        return redirect('/login')  # Redirect to the login page or handle it appropriately

    # Fetch user's existing information from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (user_email,))
    user_info = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        # Extract additional data from the profile form submission
        age = request.form['age']
        gender = request.form['gender']
        dob = request.form['dob']
        telephone = request.form['telephone']
        level_of_education = request.form['level_of_education']
        courses_enrolled = request.form['courses_enrolled']
        about_me = request.form['about_me']
        mentor = request.form['mentor']
        notification = 'Yes' if 'notification' in request.form else 'No'
        calendar = request.form['calendar']

        # Update the additional data in the users table in the database
        conn = get_db_connection()
        conn.execute('''UPDATE users SET age=?, gender=?, dob=?, telephone=?, level_of_education=?,
                        courses_enrolled=?, about_me=?, mentor=?, notification=?, calendar=?
                        WHERE email=?''',
                     (age, gender, dob, telephone, level_of_education, courses_enrolled,
                      about_me, mentor, notification, calendar, user_email))
        conn.commit()
        conn.close()

        # Redirect to a success page or any other page as needed
        return redirect('/profile')  # You can change this redirection as per your requirement

    # Render the profile page template, passing the user's existing information
    return render_template('profile.html', user_info=user_info)

# Logout route
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # Clear the user's session
    session.pop('email', None)
    logout_user()  # Log out the user
    # Redirect to the login page
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
