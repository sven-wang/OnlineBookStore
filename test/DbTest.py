#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all the imports
import MySQLdb
import config
import dbconnect
import dbOperation
import sys
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.config.from_object(__name__)
app.config.update(dict(SECRET_KEY='development key'))

def connect_db():
    """Connects to the specific database."""
    try:
        db = MySQLdb.connect("localhost", config.USERNAME, config.PASSWORD, config.SCHEMA)
        #print 'Connected Successfully'
    except Exception as ex:
        print 'Failed'
        raise Exception("Fail to connect to database: "+ex.__str__())
    return db


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = dbconnect.dbConnect()
    return g.mysql_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    db.insertDB('INSERT INTO Customers(login_name, full_name, passwords, card_num, address, phone_num) '
                'VALUES ("1234", "1234", "1234", "1234", "1234", "1234")')

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'

# @app.route('/')
# def show_entries():
#     db = get_db()
#     entries = db.readDB('select login_name, passwords, card_num from Customers')
#     return render_template('login.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.insertDB('INSERT INTO Customers(login_name, full_name, passwords, card_num, address, phone_num) '
                'VALUES (\'%s\', \'123456\', \'%s\', \'%s\', \'123456\', \'123456\')'
                % (request.form['name'], request.form['pass'], request.form['card']))
    flash('New Customers was successfully added')
    return redirect(url_for('show_entries'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    #message = None
    if request.method == 'POST':
        if request.form['btn'] == 'Login':
            db = get_db()
            user = db.readDB('select count(*) from Customers where login_name = \'%s\' and passwords = \'%s\''
                             % (request.form['login_name'], request.form['passwords']))
            if user[0][0] == 0L:
                error = 'Invalid'
            else:
                session['logged_in'] = True
                session['username'] = request.form['login_name']
                # print session['username']
                flash('You were logged in. BuyLah！')
                return redirect(url_for('search'))
        if request.form['btn'] == 'Create':
            # print 123456789
            db = dbOperation.dbOperation()
            db.registration(request.form['login_name'], request.form['full_name'], request.form['passwords'], request.form['card_num'], request.form['address'], request.form['phone_num'])
            #message = 'Create Successfully'
            return redirect(url_for('login'))
        return render_template('error.html')
    return render_template('HomePage.html', error=error)

# @app.route('/submit', methods=['POST'])
# def submit():
#     error = None
#     if request.method == 'POST':
#         db = get_db()
#         db.insertDB('INSERT INTO Customers(login_name, full_name, passwords, card_num, address, phone_num) '
#                 'VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'
#                 % (request.form['login_name'], request.form['full_name'], request.form['passwords'], request.form['card_num'], request.form['address'], request.form['phone_num']))
#     else:
#         error = 'Invalid'

@app.route('/search', methods=['GET', 'POST'])
def search():
    entries = None
    if request.method == 'POST':
        db = dbOperation.dbOperation()
        entries = db.search(request.form['author'], request.form['publisher'], request.form['title'], request.form['subject'])
        print 12345
    return render_template('search.html', entries=entries)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.ByeLah！')
    return render_template('Logout.html')

@app.route('/bookinfo?=<string:ISBN>')
def bookinfo(ISBN):
    db = dbOperation.dbOperation()
    info = db.searchISBN(ISBN)
    feedback = db.getFeedback(ISBN)
    return render_template('BookInfo.html', BookInfo=info[0], FeedBack=feedback)

@app.route('/user?=<string:USERNAME>')
def userpage(USERNAME):
    db = dbOperation.dbOperation()
    account_info, order_history, feedback_history, feedback_rate = db.userRecord_temp(USERNAME)
    return render_template('UserPage.html', A=account_info, O=order_history, H=feedback_history, R=feedback_rate)

@app.route('/cart')
def cart():

    return render_template('Cart.html')

