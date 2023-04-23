import ast

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3 as sql
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
        print(session['user_type'])
        if session['user_type'] == 'Seller':
            return render_template('seller/index.html', user=session['email'])
        elif session['user_type'] == 'Bidder':
            print(auction_listings())
            auctions = auction_listings()
            categories = parent_categories()
            print(categories)
            return render_template('bidder/index.html', user=session['email'], auctions=auctions, categories=categories)
        elif session['user_type'] == 'Helpdesk':
            return render_template('helpdesk/index.html', user=session['email'])
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
        user_type = request.form['user_type']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user_type == 'Seller':
            print('Seller')
            cursor.execute("SELECT Sellers.email FROM Users INNER JOIN Sellers ON Users.email = Sellers.email WHERE "
                           "Sellers.email=? AND Users.password=?", (email, hashed_password))
        elif user_type == 'Bidder':
            print('Bidder')
            cursor.execute("SELECT Bidders.email FROM Users INNER JOIN Bidders ON Users.email = Bidders.email WHERE "
                           "Bidders.email=? AND Users.password=?", (email, hashed_password))
        elif user_type == 'Helpdesk':
            print('Helpdesk')
            cursor.execute("SELECT Helpdesk.email FROM Users INNER JOIN Helpdesk ON Users.email = Helpdesk.email WHERE "
                           "Helpdesk.email=? AND Users.password=?", (email, hashed_password))
        user = cursor.fetchone()
        print(user)
        print(user_type)
        if user is not None:
            session['email'] = user[0]
            session['user_type'] = user_type
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')


# This route ends the users current session and redirects them to the login page
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('email', None)
    session.pop('user_type', None)
    return redirect('/')


# Populate Auction Table
def auction_listings():
    connection = sql.connect('database.db')
    cursor = connection.execute("SELECT * FROM Auction_Listings WHERE Status = 1;")
    return cursor.fetchall()


# Populate parent categories dropdown
def parent_categories():
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT DISTINCT parent_category FROM Categories;')
    categories = cursor.fetchall()
    category_list = [i[0] for i in categories]
    category_list.sort()
    return category_list


# Get auction listings from selected child categories in a list
def get_sub_category_auctions(sub_category_list):
    connection = sql.connect('database.db')
    query = 'SELECT * FROM Auction_Listings WHERE Auction_Listings.Category IN ({})'.format(
        ','.join('?' * len(sub_category_list)))
    auctions = connection.execute(query, sub_category_list).fetchall()
    return auctions


# Get all auctions listings from the main parent category
def get_all_sub_category_auctions(category):
    all_sub_category_list = get_sub_category_list(category)
    all_sub_category_list.append(category)
    auctions = get_sub_category_auctions(all_sub_category_list)
    return auctions


# Get list of all sub categories within a parent category
def get_sub_category_list(category):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT category_name FROM Categories WHERE parent_category = ?;', (category,))
    sub_categories = cursor.fetchall()
    all_sub_category_list = [i[0] for i in sub_categories]
    return all_sub_category_list


@app.route('/parent-filter', methods=['POST'])
def parent_filter():
    # connection = sql.connect('database.db')
    category = request.form['categoryName']
    auctions = get_all_sub_category_auctions(category)
    sub_category_list = get_sub_category_list(category)
    print(auctions)
    return render_template('bidder/products.html', user=session['email'], category=category, auctions=auctions,
                           sub_categories=sub_category_list)


# render the auction listing when a sub category(s) are selected
@app.route('/auction-sub-filter', methods=['POST'])
def auction_sub_filter():
    selected_values = request.form.getlist('sub_category')
    category = request.form['category']
    sub_categories = request.form['sub_categories']
    sub_categories_list = ast.literal_eval(sub_categories)
    print(sub_categories)
    print(selected_values)
    if len(selected_values) == 0:
        auctions = get_all_sub_category_auctions(category)
        return render_template('bidder/products.html', user=session['email'], category=category, auctions=auctions,
                               sub_categories=sub_categories_list)
    else:
        auctions = get_sub_category_auctions(selected_values)
        return render_template('bidder/products.html', user=session['email'], category=category, auctions=auctions,
                               sub_categories=sub_categories_list, selected_sub_categories=selected_values)


# Run main app
if __name__ == "__main__":  # Run main app
    app.run()
