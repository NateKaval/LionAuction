import sqlite3 as sql
from functions.listings import get_auction_listing


# bidding.py includes the functionality for bidders to bid on auctions


# Bid on auction
def bid(seller_email, bidder_email, bid_amount, listing_id):
    listing_info = get_auction_listing(seller_email, listing_id)
    print('listing info:')
    print(listing_info)
    remaining_bids = int(listing_info[11])
    max_bid = float(listing_info[10])
    bid_amount = float(bid_amount)
    print(max_bid)
    if bid_amount > (max_bid + 1) and remaining_bids != 0:
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT MAX(Bid_ID) FROM Bids')
        max_bid_id = int(cursor.fetchone()[0])
        max_bid_id += 1
        connection.execute('INSERT INTO Bids (Bid_ID, Seller_Email, Listing_ID, Bidder_email, Bid_price) VALUES (?,?,'
                           '?,?,?);', (max_bid_id, seller_email, listing_id, bidder_email, bid_amount))
        connection.commit()

        if remaining_bids == 1:
            reserve_price = float(listing_info[9])
            # set to sold listing if reserve is met status: 2
            if bid_amount > reserve_price:
                cursor.execute('UPDATE Auction_Listings SET Status = ? WHERE Seller_Email = ? AND Listing_ID = ?',
                               (2, seller_email, listing_id))
                connection.commit()
                print('ayy made reserve price')
            # set to inactive listing since it was not met status: 0
            else:
                cursor.execute('UPDATE Auction_Listings SET Status = ? WHERE Seller_Email = ? AND Listing_ID = ?',
                               (0, seller_email, listing_id))
                connection.commit()
                print('oof didnt make reserve price')
            print('your the last to bid')
            connection.close()
        elif remaining_bids > 1:
            print('theres still more to go')
    else:
        print('failed to bid you broke')
