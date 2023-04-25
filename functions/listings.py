import sqlite3 as sql


# listings.py provides functionality to find auction listings, whether that be a particular one or all of them


# Populate Auction Table
def auction_listings():
    connection = sql.connect('database.db')
    cursor = connection.execute('''
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
        WHERE Auction_Listings.Status = 1
        GROUP BY
          Auction_Listings.Listing_ID;
    ''')
    return cursor.fetchall()


# If there are no bids yet for a particular auction listing, the result of the LEFT JOIN between the Auction_Listings
# table and the Bids table will include all the rows from the Auction_Listings table, and NULL values for the columns
# of the Bids table. In this case, the MAX function will return NULL as there are no bids, and the COUNT function
# will return 0 since there are no matching rows in the Bids table.


# Find and return particular auction listing given the seller email and auction listing id
def get_auction_listing(seller_email, auction_listing_id):
    connection = sql.connect('database.db')
    cursor = connection.execute('''
        SELECT
            Auction_Listings.Listing_ID,
            Auction_Listings.Seller_Email,
            Auction_Listings.Auction_Title,
            Auction_Listings.Category,
            Auction_Listings.Product_Name,
            Auction_Listings.Product_Description,
            Auction_Listings.Quantity,
            Auction_Listings.Reserve_Price,
            Auction_Listings.Max_bids,
            Auction_Listings.Status,
            COALESCE(MAX(Bids.Bid_price), 0) AS Max_Bid_Price,
            (Auction_Listings.Max_bids - COUNT(Bids.Bid_ID)) AS Remaining_Bids,
            COUNT(Bids.Bid_ID) AS Bid_Count,
            Bids.Bidder_Email AS Highest_Bidder_Email
        FROM
            Auction_Listings
            LEFT JOIN Bids ON Auction_Listings.Listing_ID = Bids.Listing_ID
        WHERE
            Auction_Listings.Seller_Email = ?
            AND Auction_Listings.Listing_ID = ?
        GROUP BY
            Auction_Listings.Listing_ID;
    ''', (seller_email, auction_listing_id))
    return cursor.fetchone()


# Find and return all particular auction listings given the seller email
def get_auction_listings(seller_email):
    connection = sql.connect('database.db')
    cursor = connection.execute('''
        SELECT
            Auction_Listings.Listing_ID,
            Auction_Listings.Seller_Email,
            Auction_Listings.Auction_Title,
            Auction_Listings.Category,
            Auction_Listings.Product_Name,
            Auction_Listings.Product_Description,
            Auction_Listings.Quantity,
            Auction_Listings.Reserve_Price,
            Auction_Listings.Max_bids,
            Auction_Listings.Status,
            COALESCE(MAX(Bids.Bid_price), 0) AS Max_Bid_Price,
            (Auction_Listings.Max_bids - COUNT(Bids.Bid_ID)) AS Remaining_Bids,
            COUNT(Bids.Bid_ID) AS Bid_Count,
            Bids.Bidder_Email AS Highest_Bidder_Email
        FROM
            Auction_Listings
            LEFT JOIN Bids ON Auction_Listings.Listing_ID = Bids.Listing_ID
        WHERE
            Auction_Listings.Seller_Email = ?
        GROUP BY
            Auction_Listings.Listing_ID;
    ''', (seller_email,))
    return cursor.fetchall()


# Post new listing
def seller_new_listing(seller_email, category, auction_title, product_name, product_description, quantity,
                       reserve_price, max_bids):
    status = 1
    print(seller_email, category, auction_title, product_name, product_description, quantity, reserve_price, max_bids)
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT MAX(Listing_ID) FROM Auction_Listings WHERE Seller_Email = ?;', (seller_email,))
    max_listing_id = int(cursor.fetchone()[0])
    listing_id = max_listing_id + 1
    cursor.execute("INSERT INTO Auction_Listings (Seller_Email, Listing_ID, Category, Auction_Title, Product_Name, "
                   "Product_Description, Quantity, Reserve_Price, Max_bids, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "
                   "?, ?);", (seller_email, listing_id, category, auction_title, product_name, product_description,
                              quantity, reserve_price, max_bids, status))
    connection.commit()
    connection.close()

