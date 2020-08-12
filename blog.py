# blog.py - controller

# imports
import os
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
import sqlite3
from functools import wraps
import psycopg2

# configuration
DEBUG = True
HOST = 'localhost'
DATABASE = 'blogdb'
DB_USER = 'bloguser'
DB_PWD = 'flask1234'
DB_PORT = '5432'
# DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'
#SECRET_KEY = 9*\xfe\xa2\x9b5\xe1\x90Il\x89\x84\x8dD=6\xe0#\xf5@8\x94\xf4\x8e


app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# function used for connecting to the database
def connect_db():
    #return sqlite3.connect(app.config['DATABASE'])
    return psycopg2.connect(
        host=app.config['HOST'],
        database=app.config['DATABASE'],
        user=app.config['DB_USER'],
        password=app.config['DB_PWD'],
        port=app.config['DB_PORT']
    )
   
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            #flash('Invalid Credentials. Please try again.')
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error), status_code
    
@app.route('/main')
@login_required
def main():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('select * from posts')
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    conn.close()
    # g.db = connect_db()
    # cur = g.db.execute('select * from posts')
    # posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    # g.db.close()
    return render_template('main.html', posts=posts)    

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("All fields are required. Please try again.")
        return redirect(url_for('main'))
    else:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""insert into posts (title, post) values (%s, %s)""", (request.form['title'], request.form['post']))
        conn.commit()
        conn.close()
        flash('New entry was successfully posted!')
        return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))    

if __name__ == '__main__':
    #app.run(debug=True)    
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0')
