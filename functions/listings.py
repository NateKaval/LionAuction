import sqlite3 as sql


# listings.py provides functionality to find auction listings, whether that be a particular one or all of them


# Populate Auction Table
def auction_listings():
    connection = sql.connect('database.db')
    cursor = connection.execute("""
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
    """)
    return cursor.fetchall()
# If there are no bids yet for a particular auction listing, the result of the LEFT JOIN between the Auction_Listings
# table and the Bids table will include all the rows from the Auction_Listings table, and NULL values for the columns
# of the Bids table. In this case, the MAX function will return NULL as there are no bids, and the COUNT function
# will return 0 since there are no matching rows in the Bids table.


# Find and return particular auction listing given the seller email and auction listing id
def get_auction_listing(seller_email, auction_listing_id):
    connection = sql.connect('database.db')
    cursor = connection.execute('SELECT * FROM Auction_Listings WHERE Seller_Email = ? AND Listing_ID = ?;', (seller_email, auction_listing_id))
    return cursor.fetchall()
