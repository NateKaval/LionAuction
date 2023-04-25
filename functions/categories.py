import sqlite3 as sql


# Categories.py defines all the functionality to get auction listings based on the categories
# and supports app.route functions in app.py


# Populate parent categories dropdown
def parent_categories():
    connection = sql.connect('database.db')
    cursor = connection.execute("SELECT category_name FROM Categories WHERE parent_category = 'Root';")
    categories = cursor.fetchall()
    category_list = [i[0] for i in categories]
    category_list.sort()
    return category_list


# Get parent category from a sub category
def get_parent_category(category):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT parent_category FROM Categories WHERE category_name = ?;', (category,))
    parent_category = cursor.fetchone()[0]
    return parent_category


# Get auction listings from selected child categories in a list
def get_sub_category_auctions(sub_category_list):
    connection = sql.connect('database.db')
    query = """
        SELECT
          Auction_Listings.Listing_ID,
          Auction_Listings.Seller_Email,
          Auction_Listings.Auction_Title,
          Auction_Listings.Category,
          MAX(Bids.Bid_price) AS Max_Bid_Price,
          (Auction_Listings.Max_bids - COUNT(Bids.Bid_ID)) AS Remaining_Bids,
          COUNT(Bids.Bid_ID) AS Bid_Count
        FROM
          Auction_Listings
          LEFT JOIN Bids ON Auction_Listings.Listing_ID = Bids.Listing_ID
        WHERE
          Auction_Listings.Status = 1
          AND Auction_Listings.Category IN ({})
        GROUP BY
          Auction_Listings.Listing_ID;
    """.format(','.join('?' * len(sub_category_list)))
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
