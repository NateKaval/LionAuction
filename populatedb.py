import sqlite3 as sql
import csv
import hashlib

connection = sql.connect('database.db')
cursor = connection.cursor()


# Populate user table
def populate_users(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Users;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Users(email TEXT PRIMARY KEY, password TEXT NOT NULL);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        email = row[0]
        password = row[1]
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        cursor.execute('INSERT or REPLACE INTO Users (email, password) VALUES (?, ?)', (email, hashed_password))

    connection.commit()


# View all entries of a table
def view_table_entries(table_name):
    select_all = "SELECT * FROM " + f'{table_name}'
    rows = cursor.execute(select_all).fetchall()

    # Output to the console screen
    for r in rows:
        print(r)


# Populate user table
def populate_helpdesk(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Helpdesk;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Helpdesk(email TEXT PRIMARY KEY, position TEXT NOT NULL);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        email = row[0]
        position = row[1]
        cursor.execute('INSERT or REPLACE INTO Helpdesk (email, position) VALUES (?, ?)', (email, position))

    connection.commit()


# Populate user table
def populate_requests(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Requests;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Requests(request_id TEXT PRIMARY KEY, sender_email TEXT, '
                       'helpdesk_staff_email TEXT, request_type TEXT, request_desc TEXT, request_status INTEGER);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        request_id = row[0]
        sender_email = row[1]
        helpdesk_staff_email = row[2]
        request_type = row[3]
        request_desc = row[4]
        request_status = row[5]

        cursor.execute('INSERT or REPLACE INTO Requests (request_id, sender_email, helpdesk_staff_email, '
                       'request_type, request_desc, request_status) VALUES (?, ?, ?, ?, ?, ?)',
                       (request_id, sender_email,
                        helpdesk_staff_email,
                        request_type, request_desc,
                        request_status))

    connection.commit()


# Populate user table
def populate_bidders(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Bidders;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Bidders(email TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, '
                       'gender TEXT, age INTEGER, home_address_id TEXT, major TEXT);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        email = row[0]
        first_name = row[1]
        last_name = row[2]
        gender = row[3]
        age = row[4]
        home_address_id = row[5]
        major = row[6]

        cursor.execute('INSERT or REPLACE INTO Bidders (email, first_name, last_name, '
                       'gender, age, home_address_id, major) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (email, first_name,
                        last_name,
                        gender, age,
                        home_address_id, major))

    connection.commit()


# Populate credit cards table
def populate_credit_cards(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Credit_Cards;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Credit_Cards(credit_card_num TEXT PRIMARY KEY, card_type TEXT, '
                       'expire_month INTEGER, expire_year INTEGER, security_code INTEGER, owner_email TEXT, '
                       'FOREIGN KEY (Owner_email) REFERENCES Bidders(email));')

    # The Owner_email column has a foreign key constraint that references the email column of the Bidders table. This
    # ensures that each credit card is owned by only one bidder, and that an owner may have one or multiple credit
    # cards stored in the system.

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        credit_card_num = row[0]
        card_type = row[1]
        expire_month = row[2]
        expire_year = row[3]
        security_code = row[4]
        owner_email = row[5]

        cursor.execute('INSERT or REPLACE INTO Credit_Cards (credit_card_num, card_type, expire_month, '
                       'expire_year, security_code, owner_email) VALUES (?, ?, ?, ?, ?, ?)',
                       (credit_card_num, card_type, expire_month, expire_year, security_code, owner_email))

    connection.commit()


# populate_users("dataset/Users.csv")
# populate_helpdesk("dataset/Helpdesk.csv")
# populate_requests("dataset/Requests.csv")
# populate_bidders("dataset/Bidders.csv")
# view_table_entries("Bidders")
populate_credit_cards("dataset/Credit_Cards.csv")
view_table_entries("Credit_Cards")

# Close connection after all functions are performed
connection.close()
