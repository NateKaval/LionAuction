from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3 as sql
import csv
import hashlib

app = Flask(__name__)
app.secret_key = 'LionAuction'
host = 'http://127.0.0.1:5000/'


# Render the login template first
@app.route('/')
def index():
    return render_template('login.html')


# This path verifies if a user is logged in and returns the home page
# If the user is not logged in, they are redirected to the login page
@app.route('/home')
def home():
    if 'email' in session:
        return render_template('index.html', user=session['email'])
    return redirect(url_for('login'))


# Create route /login to be used to log in to Lion Auction
# get email and password fields from form
# hash password and search users database
# if the user info is found create a session
# if the user info is incorrect add message to index template
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        email = request.form['Email']
        password = request.form['Password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hashed_password))
        user = cursor.fetchone()
        print(user)
        if user is not None:
            session['email'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')


# This route ends the users current session and redirects them to the log in page
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('email', None)
    return redirect('/')

# connection = sql.connect('database.db')
# cursor = connection.cursor()
# connection.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, password TEXT NOT NULL);')
#
# user_file = open('users.csv', encoding='utf-8-sig')
# users = csv.reader(user_file)
#
# for row in users:
#     email = row[0]
#     password = row[1]
#     hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
#     cursor.execute('INSERT or REPLACE INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
# select_all = "SELECT * FROM users"
# rows = cursor.execute(select_all).fetchall()
# # Output to the console screen
# for r in rows:
#     print(r)
# connection.commit()


# Run main app
if __name__ == "__main__":  # Run main app
    app.run()
