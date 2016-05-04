# sql.py - to create SQLite3 table with two fields

import sqlite3


# create a new database 
with sqlite3.connect("blog.db") as connection:

	# get the cursor object to execute SQL commands
	c = connection.cursor()


	# create Table with two fields
	# c.execute("""CREATE TABLE posts (title TEXT, post TEXT)""")


	# insert dummy data to the table
	c.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')                    
	c.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
	c.execute('INSERT INTO posts VALUES("Fine", "I\'m fine.")')
	c.execute('INSERT INTO posts VALUES("Okay", "I\'m okay.")')

