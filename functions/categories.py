import sqlite3 as sql

# Categories.py defines all the functionality to get auction listings based on the categories
# and supports app.route functions in app.py


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