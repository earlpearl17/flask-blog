# sql.py - Create a SQLite3 table and populate it with data

import sqlite3

# create a new database if the database doesn't already exist
with sqlite3.connect("blog.db") as connection:

    # get a cursor object to execute SQL commands
    c = connection.cursor()

    # check if posts table already exists
    c.execute('DROP TABLE IF EXISTS posts')

    # create the posts table
    c.execute("""CREATE TABLE IF NOT EXISTS posts 
                (title TEXT, post TEXT)
              """)

    # insert dummy data into the table
    c.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
    c.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
    c.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.")')
    c.execute('INSERT INTO posts VALUES("Okay", "I\'m okay.")')