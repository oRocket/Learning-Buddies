#!/usr/bin/python3

import sqlite3

def print_database():
    conn = sqlite3.connect('learning-buddies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    
    for row in rows:
        print(f'ID: {row[0]}')
        print(f'First Name: {row[1]}')
        print(f'Last Name: {row[2]}')
        print(f'Email: {row[3]}')
        print(f'New Password: {row[4]}')
        print(f'Confirm Password: {row[5]}')
        print('-------------------')
    
    conn.close()

if __name__ == '__main__':
    print_database()
