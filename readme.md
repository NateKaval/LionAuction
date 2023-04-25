# Lion Auction

---

_Created by Nathaniel Kaval_

Scenario: You are assigned to design the website called Lion Auction that will allow
students and other businesses to auction and bid on items.  i) context of your code (i.e., background information such as what they are used for); ii)
features (i.e., functions/operations of the codes); iii) organization (i.e., how the files are organized);
iv) instructions (i.e., how to run the code, including how and where to load the files into PyCharm
Professional).

## Getting Started

* Ensure you have flask installed
* To run application, run app.py

## Task 1 Login Page Functionality: 

1. **First populate database with users emails and passwords**

Completed by connecting to database and the csv import to parse through the csv file. Next, goes through
each row and hashes the passwords using the hashlib library to hash the password using SHA256.

2. **Next users need to Log in**

Completed by taking the users input and hashing the password to then create a query to
search through the database to find the entry. If the user entry is found a session is created
using the email. However, if the user entry is not found an error message will then be passed 
to the login page render to inform the user has entered an incorrect password.

3. **Login Failure**

When a user enters the wrong username and password combo an error message is passed to the login html page
to inform the user they have used incorrect information.

4. **Login Success**

When a user has correctly logged in, the home page will then display with the users email
in the right hand corner of the nav bar. 

5. **Log out**

In order to log out a route is created to link to the sign-out button that ends the current users
session.

## Task 2 Category Browsing:

1. **Users can view current parent directory**

Completed by populating a dropdown with all the root categories. Then recursively calling those
categories to populate the auction results

2. **User can click on auction listing**

When a user clicks on the auction listing it will then render a page for that listing and 
allow them to view the information along with being able to bid

## Task 3 Auction Listing:

1. **Seller can view their listings**

On the main seller page they can view their current, past, and inactive listings

2. **Seller can post new listing**

On the nav bar a seller can click new posting and then fill out the information needed for the 
new auction listing and it will add to the auction listings table

## Task 4 Bidding

1. **A bidder can bid on an item**

When a bidder finds a listing they would like to bid on, they can do so by putting in 
the amount they'd like to bid. Once that goes through they can't bid again til someone else 
does.