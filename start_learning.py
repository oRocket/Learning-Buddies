#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask import flash
import json
from flask import jsonify

app = Flask(__name__)
app.secret_key = ']!B+M5`sO@8Hgl[m?2,>RMI}'

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning-buddies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    confirm_password = db.Column(db.String(100), nullable=False)

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        # If the user is already authenticated, redirect to the profile page
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        # Process form submission
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        confirm_password = request.form['confirm_password']

        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', error='Email already exists. Please choose another email.')

        # Create a new user instance
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password, confirm_password=confirm_password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user
        login_user(new_user)

        # Redirect to the profile page after successful signup
        return redirect(url_for('profile'))

    # For GET requests or if there's no form submission yet, render the signup page
    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve user from the database
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Authentication successful, load the user and log them in
            login_user(user)
            session['email'] = email
            return redirect(url_for('profile'))
        else:
            # Authentication failed, render login page with error message
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

# Update the /profile route to handle both GET and POST methods
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Ensure the request data is in JSON format
        if request.is_json:
            data = request.get_json()

            # Update user profile with the received data
            current_user.first_name = data.get('first_name', current_user.first_name)
            current_user.last_name = data.get('last_name', current_user.last_name)
            current_user.email = data.get('email', current_user.email)

            # Add more fields here as needed

            # Commit changes to the database
            db.session.commit()

            # Respond with a success message
            return jsonify({'message': 'Profile updated successfully'}), 200

        # If the request data is not in JSON format, respond with an error
        return jsonify({'error': 'Invalid JSON data'}), 400

    # For GET requests, render the profile page
    return render_template('profile.html', user=current_user)


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    return render_template('courses.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        # Perform logout actions
        session.pop('email', None)
        logout_user()
        return redirect(url_for('login'))

    # For GET requests, redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    # Ensure database initialization and migration
    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)
        
        # Apply any pending migrations
        db.session.commit()

    app.run(debug=True)
