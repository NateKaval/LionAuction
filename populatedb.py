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
    connection.execute('CREATE TABLE IF NOT EXISTS Helpdesk(email TEXT PRIMARY KEY, position TEXT NOT NULL, '
                       'FOREIGN KEY(email) REFERENCES Users(email));')

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
    connection.execute(
        'CREATE TABLE IF NOT EXISTS Requests(request_id TEXT PRIMARY KEY, sender_email TEXT, helpdesk_staff_email '
        'TEXT, request_type TEXT, request_desc TEXT, request_status INTEGER, FOREIGN KEY(helpdesk_staff_email)'
        ' REFERENCES Helpdesk(email), FOREIGN KEY(sender_email) REFERENCES Users(email));')

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
    connection.execute('CREATE TABLE IF NOT EXISTS Bidders(email TEXT PRIMARY KEY REFERENCES Users(email), first_name '
                       'TEXT, last_name TEXT, gender TEXT, age INTEGER, home_address_id TEXT, major TEXT);')

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
                       'FOREIGN KEY (owner_email) REFERENCES Bidders(email));')

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


# Populate address table
def populate_address(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Address;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Address(address_ID TEXT PRIMARY KEY, zipcode TEXT, '
                       'street_num TEXT, street_name TEXT);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        address_id = row[0]
        zipcode = row[1]
        street_num = row[2]
        street_name = row[3]

        cursor.execute('INSERT or REPLACE INTO Address (address_ID, zipcode, street_num, street_name) VALUES (?, ?, '
                       '?, ?)',
                       (address_id, zipcode, street_num, street_name))

    connection.commit()


# Populate Zipcode_Info table
def populate_zipcode_info(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Zipcode_Info;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Zipcode_Info(zipcode TEXT PRIMARY KEY, city TEXT, state TEXT);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        zipcode = row[0]
        city = row[1]
        state = row[2]

        cursor.execute('INSERT or REPLACE INTO Zipcode_Info (zipcode, city, state) VALUES (?, ?, ?)',
                       (zipcode, city, state))

    connection.commit()


# Populate Sellers table
def populate_sellers(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Sellers;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Sellers(email TEXT PRIMARY KEY, bank_routing_number TEXT, '
                       'bank_account_number TEXT, balance FLOAT, FOREIGN KEY(email) REFERENCES Users(email));')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        email = row[0]
        bank_routing_number = row[1]
        bank_account_number = row[2]
        balance = row[3]

        cursor.execute('INSERT or REPLACE INTO Sellers (email, bank_routing_number, bank_account_number, balance) '
                       'VALUES (?, ?, ?, ?)', (email, bank_routing_number, bank_account_number, balance))

    connection.commit()


# Populate Local_Vendors table
def populate_local_vendors(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS local_vendors;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS local_vendors(email TEXT PRIMARY KEY, business_name TEXT, '
                       'business_address_id TEXT,customer_service_phone_number TEXT, FOREIGN KEY(email) REFERENCES'
                       ' Sellers(email));')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        email = row[0]
        business_name = row[1]
        business_address_id = row[2]
        customer_service_phone_number = row[3]

        cursor.execute('INSERT or REPLACE INTO local_vendors (email, business_name, business_address_id, '
                       'customer_service_phone_number) VALUES (?, ?, ?, ?)',
                       (email, business_name, business_address_id, customer_service_phone_number))

    connection.commit()


# Populate categories table
def populate_categories(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Categories;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Categories(parent_category TEXT, category_name TEXT PRIMARY KEY);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        parent_category = row[0]
        category_name = row[1]

        cursor.execute('INSERT or REPLACE INTO Categories (parent_category, category_name) VALUES (?, ?)',
                       (parent_category, category_name))

    connection.commit()


# Populate Auction_Listings table
def populate_auction_listings(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Auction_Listings;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Auction_Listings(Seller_Email TEXT, Listing_ID INTEGER, '
                       'Category TEXT, Auction_Title TEXT, Product_Name TEXT, Product_Description TEXT, '
                       'Quantity INTEGER, Reserve_Price REAL, Max_bids INTEGER, Status TEXT, '
                       'PRIMARY KEY (Seller_Email, Listing_ID));')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        seller_email = row[0]
        listing_id = row[1]
        category = row[2]
        auction_title = row[3]
        product_name = row[4]
        product_description = row[5]
        quantity = row[6]
        reserve_price = row[7]
        max_bids = row[8]
        status = row[9]

        cursor.execute('INSERT or REPLACE INTO Auction_Listings (Seller_Email, Listing_ID, Category, Auction_Title, '
                       'Product_Name, Product_Description, Quantity, Reserve_Price, Max_bids, Status) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (seller_email, listing_id, category, auction_title, product_name, product_description,
                        quantity, reserve_price, max_bids, status))

    connection.commit()


def populate_bids(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Bids;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Bids(Bid_ID INTEGER PRIMARY KEY, Seller_Email TEXT, Listing_ID '
                       'INTEGER, Bidder_email TEXT, Bid_price INTEGER, '
                       'FOREIGN KEY(Listing_ID) REFERENCES Auction_Listings(Listing_ID));')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        bid_id = row[0]
        seller_email = row[1]
        listing_id = row[2]
        bidder_email = row[3]
        bid_price = row[4]

        cursor.execute('INSERT or REPLACE INTO Bids (Bid_ID, Seller_Email, Listing_ID, Bidder_email, Bid_price) '
                       'VALUES (?, ?, ?, ?, ?)',
                       (bid_id, seller_email, listing_id, bidder_email, bid_price))

    connection.commit()


# Populate Transactions table
def populate_transactions(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Transactions;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Transactions(Transaction_ID INTEGER PRIMARY KEY, '
                       'Seller_Email TEXT, Listing_ID TEXT, Buyer_Email TEXT, Date TEXT, Payment REAL);')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        transaction_id = row[0]
        seller_email = row[1]
        listing_id = row[2]
        buyer_email = row[3]
        date = row[4]
        payment = row[5]

        cursor.execute('INSERT or REPLACE INTO Transactions (Transaction_ID, Seller_Email, Listing_ID, '
                       'Buyer_Email, Date, Payment) VALUES (?, ?, ?, ?, ?, ?)',
                       (transaction_id, seller_email,
                        listing_id,
                        buyer_email, date,
                        payment))

    connection.commit()


# Populate rating table
def populate_rating(file):
    # Drop table if it exists
    connection.execute('DROP TABLE IF EXISTS Rating;')

    # Create table if it doesn't exist
    connection.execute('CREATE TABLE IF NOT EXISTS Rating(Bidder_Email TEXT, Seller_Email TEXT, '
                       'Date TEXT, Rating INTEGER, Rating_Desc TEXT, '
                       'PRIMARY KEY(Bidder_Email, Seller_Email, Date));')

    # Open csv file
    csv_file = open(f'{file}', encoding='utf-8-sig')
    data = csv.reader(csv_file)

    # Skip the first line of the CSV file
    next(data)

    for row in data:
        bidder_email = row[0]
        seller_email = row[1]
        date = row[2]
        rating = row[3]
        rating_desc = row[4]

        cursor.execute('INSERT or REPLACE INTO Rating (Bidder_Email, Seller_Email, Date, Rating, Rating_Desc) '
                       'VALUES (?, ?, ?, ?, ?)',
                       (bidder_email, seller_email, date, rating, rating_desc))

    connection.commit()


populate_users("dataset/Users.csv")
populate_helpdesk("dataset/Helpdesk.csv")
populate_requests("dataset/Requests.csv")
populate_bidders("dataset/Bidders.csv")
# view_table_entries("Bidders")
populate_credit_cards("dataset/Credit_Cards.csv")
populate_address("dataset/Address.csv")
populate_zipcode_info("dataset/Zipcode_Info.csv")
populate_sellers("dataset/Sellers.csv")
populate_local_vendors("dataset/Local_Vendors.csv")
populate_categories("dataset/Categories.csv")
populate_auction_listings("dataset/Auction_Listings.csv")
populate_bids("dataset/Bids.csv")
populate_transactions("dataset/Transactions.csv")
populate_rating("dataset/Ratings.csv")


view_table_entries("Bids")

# Close connection after all functions are performed
connection.close()
