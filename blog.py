# blog.py - controller

# imports
from flask import Flask, render_template, request, session, \
 flash, redirect, url_for, g
import sqlite3
from functools import wraps


# configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = '\xb2yX\x0f\x1b\x8a\xec\xe2i\xae\xfe{E\x0e\xd3\x94\xef\x8c6a\xc8\xdc\xd5\xb6'


app = Flask(__name__)


# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)


# function for connecting to the database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


# routes

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap




@app.route('/', methods=['GET', 'POST'])
def login():
	error = None

	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or \
			request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credential. Please try again.'
		else: 
			session['logged_in'] = True
			return redirect(url_for('main'))

	return render_template('login.html', error=error)



@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))



@app.route('/main')
@login_required
def main():
	
	# connect to the database
	g.db = connect_db()

	cur = g.db.execute('SELECT * from posts')

	posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
	g.db.close()

	return render_template('main.html', posts=posts)



@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']

	if not title or not post:
		flash('All fields are required. Please try again')

	else:
		g.db = connect_db()
		g.db.execute('INSERT into posts (title, post) values (?,?)', 
			[request.form['title'], request.form['post']])
		g.db.commit()
		g.db.close()
		flash('New entry was sucessfully posted!')
		return redirect(url_for('main'))



if __name__ == '__main__':
	app.run(debug=True)






