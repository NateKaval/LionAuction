
import ast
import hashlib

from flask import Flask, render_template, request, session, redirect, url_for

from functions.categories import *

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
            cursor.execute("SELECT Sellers.email FROM Users INNER JOIN Sellers ON Users.email = Sellers.email WHERE "
                           "Sellers.email=? AND Users.password=?", (email, hashed_password))
        elif user_type == 'Bidder':
            cursor.execute("SELECT Bidders.email FROM Users INNER JOIN Bidders ON Users.email = Bidders.email WHERE "
                           "Bidders.email=? AND Users.password=?", (email, hashed_password))
        elif user_type == 'Helpdesk':
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


# This route render the template for all auction listings from the category selected in the category dropdown
# Uses the get_all_sub_category_auctions function to get all auctions from the category
# Then get the sub category list from the get_sub_category_list function given a category
@app.route('/parent-filter', methods=['POST'])
def parent_filter():
    category = request.form['categoryName']
    auctions = get_all_sub_category_auctions(category)
    sub_category_list = get_sub_category_list(category)
    return render_template('bidder/products.html', user=session['email'], category=category, auctions=auctions,
                           sub_categories=sub_category_list)


# render the auction listing when a sub category(s) are selected
@app.route('/auction-sub-filter', methods=['POST'])
def auction_sub_filter():
    selected_values = request.form.getlist('sub_category')
    category = request.form['category']
    sub_categories = request.form['sub_categories']
    sub_categories_list = ast.literal_eval(sub_categories)
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
