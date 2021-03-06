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

# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.insertDB('INSERT INTO Customers(login_name, full_name, passwords, card_num, address, phone_num) '
#                 'VALUES (\'%s\', \'123456\', \'%s\', \'%s\', \'123456\', \'123456\')'
#                 % (request.form['name'], request.form['pass'], request.form['card']))
#     flash('New Customers was successfully added')
#     return redirect(url_for('show_entries'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    #message = None
    if request.method == 'POST':
        if request.form['btn'] == 'Login':
            db = get_db()
            # 过滤非法字符
            if "\'" in request.form['login_name']:
                error = "no \'"
                return render_template('HomePage.html', error=error)
            user = db.readDB('select count(*) from Customers where login_name = \'%s\' and passwords = \'%s\''
                             % (request.form['login_name'], request.form['passwords']))
            # 没有此用户名
            if user[0][0] == 0L:
                error = "Invalid"
            else:
                session['logged_in'] = True
                session['username'] = request.form['login_name']
                # print session['username']
                flash('You were logged in. BuyLah！')
                return redirect(url_for('search'))
        elif request.form['btn'] == 'Create':
            db = get_db()
            duplicated = db.readDB('select count(*) from Customers where login_name = \'%s\' or card_num = \'%s\''
                             % (request.form['login_name'], request.form['card_num']))
            print duplicated
            if duplicated[0][0] == 0L:
                db = dbOperation.dbOperation()
                db.registration(request.form['login_name'], request.form['full_name'], request.form['passwords'], request.form['card_num'], request.form['address'], request.form['phone_num'])
                # message = 'Create Successfully'
                return redirect(url_for('login'))
            else:
                error = "Duplicated Login name or card number! Please pick up another one and try again!"
                return render_template('HomePage.html', error=error)
        else:
            return render_template('error.html')
    return render_template('HomePage.html', error=error)

@app.route('/search', methods=['GET', 'POST'])
def search():
    entries = None
    if request.method == 'POST':
        db = dbOperation.dbOperation()
        entries = db.search(request.form['author'], request.form['publisher'], request.form['title'], request.form['subject'], request.form['order'], request.form['sequence'])
        # print entries

    return render_template('Search.html', entries=entries)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('manager_logged_in', None)
    flash('You were logged out.ByeLah！')
    return render_template('Logout.html')

@app.route('/bookinfo?=<string:ISBN>', methods=['GET', 'POST'])
def bookinfo(ISBN):
    error = None
    nfeedback = 5
    db = dbOperation.dbOperation()
    info = db.searchISBN(ISBN)
    feedback = db.feedBackRank(ISBN, nfeedback)
    if feedback == None:
        feedback = []
    if request.method == 'POST':
        if request.form['btn'] == 'Add to Cart!':
            if int(request.form['copies']) > int(info[0][5]):
                error = "not enough copies"
                return render_template('BookInfo.html', BookInfo=info[0], FeedBack=feedback, error=error)
            elif int(request.form['copies']) <= 0:
                error = "Please enter an integer greater than 0"
                return render_template('BookInfo.html', BookInfo=info[0], FeedBack=feedback, error=error)
            db.ordering(session['username'], ISBN, request.form['copies'])
            return redirect(url_for('recommendation', ISBN=ISBN))
        elif request.form['btn'] == 'Submit':
            db.feedBack(session['username'], ISBN,  request.form['score'] ,request.form['feedback'])
            return redirect(url_for('bookinfo', ISBN=ISBN))
        elif request.form['btn'] == 'Rate!':
            if session['username'] == request.form['fbn']:
                error = "You can't rate for feedback created by yourself!"
                return render_template('BookInfo.html', BookInfo=info[0], FeedBack=feedback, error=error)
            db.rate(session['username'], request.form['fbn'], request.form['ISBN'], request.form['scores'])
            return redirect(url_for('bookinfo', ISBN=ISBN))
        elif request.form['btn'] == 'Confirm':
            if int(request.form['num']) < 1:
                error = "Please enter a number above 1!!!"
                return render_template('BookInfo.html', BookInfo=info[0], FeedBack=feedback, error=error)
            feedback = db.feedBackRank(ISBN, request.form['num'])
    return render_template('BookInfo.html', BookInfo=info[0], FeedBack=feedback, error=error)

@app.route('/user')
def userpage():
    error = None
    db = dbOperation.dbOperation()
    account_info, order_history, feedback_history, feedback_rate = db.userRecord(session['username'])
    if order_history == None:
        order_history = []
    if feedback_history == None:
        feedback_history = []
    if feedback_rate == None:
        feedback_rate = []
    return render_template('UserPage.html', A=account_info[0], O=order_history, H=feedback_history, R=feedback_rate, error=error)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    error = None
    db = dbOperation.dbOperation()
    orderid, cart = db.viewCart(session['username'])
    if request.method == 'POST':
        db.checkOut(request.form['oid'])
        return redirect(url_for('search'))
    return render_template('Cart.html', orders=cart, orderid=orderid, error=error)

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    if request.method == 'POST':
        if request.form['btn'] == 'login':
            db = get_db()
            user = db.readDB('select count(*) from Managers where login_name = \'%s\' and passwords = \'%s\''
                             % (request.form['managername'], request.form['password']))
            if user[0][0] == 0L:
                error = 'Invalid'
            else:
                session['manager_logged_in'] = True
                session['managername'] = request.form['managername']
                # print session['username']
                flash('You were logged in. ManaLah！')
                return redirect(url_for('backstage'))
    return render_template('Manager.html')


@app.route('/backstage', methods=['GET', 'POST'])
def backstage(m=5):
    db = dbOperation.dbOperation()
    books = db.popularBooks(m)
    authors = db.popularAuthors(m)
    publishers = db.popularPublishers(m)
    if request.method == 'POST':
        if request.form['btn'] == "Submit":
            db.newArrival(request.form['isbn'], request.form['copies'])
        elif request.form['btn'] == "Confirm":
            books = db.popularBooks(request.form['num'])
            authors = db.popularAuthors(request.form['num'])
            publishers = db.popularPublishers(request.form['num'])
    return render_template('BackStage.html', books=books, authors=authors, publishers=publishers)

@app.route('/newbook', methods=['GET', 'POST'])
def newbook():
    db = dbOperation.dbOperation()
    if request.method == 'POST':
        db.newBook(request.form['isbn'], request.form['title'], request.form['authors'], request.form['publisher'], request.form['year'], request.form['copies'], request.form['price'], request.form['format'], request.form['keywords'], request.form['subject'])
    return render_template('NewBook.html')

@app.route('/recommendation?=<string:ISBN>')
def recommendation(ISBN):
    db = dbOperation.dbOperation()
    rec=db.getRecommendation(ISBN, session['username'])
    if rec == None:
        rec = []
    return render_template('Recommendation.html', rec=rec)