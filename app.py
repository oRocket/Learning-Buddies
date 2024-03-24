#!/usr/bin/python3


from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(_name_)

# Connect to SQLite3 database
conn = sqlite3.connect('learningbuddies.db')
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        new_password TEXT NOT NULL,
        confirm_password TEXT NOT NULL
    )
''')
conn.commit()

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, new_password, confirm_password)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, new_password, confirm_password))
        conn.commit()

        return redirect('/')

if _name_ == '_main_':
    app.run(debug=True)
