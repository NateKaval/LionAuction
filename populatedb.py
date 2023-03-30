import sqlite3 as sql
import csv
import hashlib

connection = sql.connect('database.db')
cursor = connection.cursor()


# Populate user table
def populate_users(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS users;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, password TEXT NOT NULL);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        email = row[0]
        password = row[1]
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        cursor.execute('INSERT or REPLACE INTO users (email, password) VALUES (?, ?)', (email, hashed_password))

    select_all = "SELECT * FROM users"
    rows = cursor.execute(select_all).fetchall()

    # Output to the console screen
    for r in rows:
        print(r)

    connection.commit()


populate_users("users.csv")

# Close connection after all functions are performed
connection.close()
