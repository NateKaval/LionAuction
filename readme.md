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