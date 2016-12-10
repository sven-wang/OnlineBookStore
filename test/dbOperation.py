import dbconnect
import datetime

class dbOperation:
    #Fuction 1: Registration
    def registration(self, login_name, full_name, passwords, card_num, address, phone_num):
        query = "INSERT INTO Customers (login_name, full_name, passwords, card_num, address, phone_num) " \
                "VALUES ('"+login_name+"', '"+full_name+"', '"+passwords+"', '"+card_num+"', '"+address+"', '"+phone_num+"');"
        try:
            db = dbconnect.dbConnect()
            db.insertDB(query)
        except Exception as ex:
            print ex.message

    # Function 2: Ordering
    def getBookName(self, ISBN):
        query = "SELECT title " \
                "FROM Books " \
                "WHERE ISBN = '" + ISBN + "';"
        try:
            db = dbconnect.dbConnect()
            return db.readDB(query)
        except Exception as ex:
            print ex.message

    def ordering(self, login_name, ISBN, copies):
        print 'def ordering'
        # check curent order status
        query1 = "SELECT status " \
                 "FROM (SELECT status, oid " \
                        "FROM Orders " \
                        "WHERE login_name = '" + login_name + "') userOrders " \
                 "ORDER BY oid DESC LIMIT 1"


        # get global max oid
        query2 = "SELECT MAX(oid) FROM Orders"
        # get user's max oid
        query3 = "SELECT MAX(oid) " \
                 "FROM Orders " \
                 "WHERE login_name = '" + login_name + "';"

        try:
            db = dbconnect.dbConnect()
            # checking user's current order status first
            status = db.readDB(query1)
            print status


            if status[0][0] == 'Complete':

                # get global max oid
                oid = db.readDB(query2)[0][0]
                # allocate a new oid
                oid = str(long(oid) + 1)
                # insert a new order
                db.insertDB("INSERT INTO Orders VALUES (" + oid + ", '" + login_name + "', CURDATE(), 'Processing')")
                # insert a new item under this oid
                db.insertDB("INSERT INTO Items VALUES (" + oid + ", '" + ISBN + "', " + copies + ")")

            if status[0][0] == 'Processing':

                # get user's current max id
                oid = str(db.readDB(query3)[0][0])
                print oid

                # insert new item
                db.insertDB("INSERT INTO Items VALUES (" + oid + ", '" + ISBN + "', " + copies + ")")
        except Exception as ex:
            print ex.message

    def viewCart(self, login_name):
        query = "SELECT Books.ISBN, title, authors, publisher, year, price, format, subject, info.copies \
                    FROM (SELECT ISBN, copies \
                    FROM Items i \
                    WHERE i. oid = (SELECT MAX(oid) \
                    FROM Orders \
                    WHERE login_name = " + login_name + " AND status = 'Processing')) info, Books \
                    WHERE info.ISBN = Books.ISBN"

        queryOid = "SELECT MAX(oid) \
                    FROM Orders \
                    WHERE login_name = " + login_name + " AND status = 'Processing'"
        try:
            db = dbconnect.dbConnect()
            oid = db.readDB(queryOid)
            items = db.readDB(query)
            return oid, items
        except Exception as ex:
            print ex.message

    def checkOut(self, oid):

        query = "UPDATE Orders " \
                "SET status = 'Complete' , date = CURDATE() " + \
                "WHERE oid = " + oid


        try:
            db = dbconnect.dbConnect()
            db.updateDB(query)
            print 'checkout'
        except Exception as ex:
            print ex.message


    #Function 3: User Record
    def userRecord(self, login_name):
        # his/her account information
        query1 = "SELECT * " \
                 "FROM Customers " \
                 "WHERE login_name = " + "'" + login_name + "';"

        # his/her full history of orders
        query2 = "SELECT oid, date, title, info.copies \
                    FROM (SELECT oid, date, ISBN, copies \
                          FROM Orders o NATURAL JOIN Items i \
                          WHERE login_name = " + login_name + ") info, Books \
                    WHERE info.ISBN = Books.ISBN "

        # his/her full history of feedbacks
        query3 = "SELECT * " \
                 "FROM Feedbacks " \
                 "WHERE login_name = " + "'" + login_name + "';"

        # the list of all the feedbacks he/she ranked with respect to usefulness
        query4 = "SELECT * " \
                 "FROM Feedbacks f, Rate r " \
                 "WHERE r.feedback_name = " + "'" + login_name + "' AND r.feedback_name = f.login_name AND f.ISBN = r.ISBN;"

        try:
            db = dbconnect.dbConnect()
            account_info = db.readDB(query1)
            order_history = db.readDB(query2)
            feedback_history = db.readDB(query3)
            feedback_rate = db.readDB(query4)
            return account_info, order_history, feedback_history, feedback_rate
        except Exception as ex:
            print ex.message

    #Function 4: New book
    def newBook(self, ISBN, title, authors, publisher, year, copies, price, format, keywords, subject):
        query = "INSERT INTO Books " \
                "VALUES ('"+ISBN+"', '"+title+"', '"+authors+"', '"+publisher+"', "+year+", "+copies+", " \
                +price+", '"+format+"', '"+keywords+"', '"+subject+"');"
        try:
            db = dbconnect.dbConnect()
            db.insertDB(query)
        except Exception as ex:
            print ex.message

    #Function 5: Arrival of more copies
    def newArrival(self, ISBN, copies):
        query = "UPDATE Books " \
                "SET copies = copies + "+copies+ \
                "WHERE ISBN = '"+ISBN+"';"
        try:
            db = dbconnect.dbConnect()
            db.updateDB(query)
        except Exception as ex:
            print ex.message

    #Function 6: Feedback recordings
    def feedBack(self, login_name, ISBN, score, text):
        query = "INSERT INTO Feedbacks " \
                "VALUES ('"+login_name+"', '"+ISBN+"', CURDATE() , "+score+", '"+text+"');"
        insertRate = "INSERT INTO Rate VALUES ('"+ login_name +"', '" + login_name + "', '"+ISBN+"', 0 )"
        try:
            db = dbconnect.dbConnect()
            db.insertDB(query)
            db.insertDB(insertRate)
        except Exception as ex:
            print ex.message

    #Function 7: Usefulness ratings
    def rate(self, rater_name, feedback_name, ISBN, usefulness):
        query = "INSERT INTO Rate " \
                "VALUES ('"+rater_name+"', '"+feedback_name+"', '"+ISBN+"', '"+usefulness+"');"

        try:
            db = dbconnect.dbConnect()
            db.insertDB(query)
        except Exception as ex:
            print ex.message

    #Function 8: Book Browsing
    def search(self, authors, publisher, title, subject, sortBy, Desc_Asc):
        authors = authors.strip()
        publisher = publisher.strip()
        title = title.strip()
        subject = subject.strip()

        query = "SELECT Books.ISBN, title, authors, publisher, year, copies, price, format,keywords, subject, AVG(score)\
                  FROM Books left join Feedbacks on Books.ISBN = Feedbacks.ISBN"

        if (authors != ''):
            query += " WHERE LOWER(authors) LIKE LOWER('%" + authors + "%')"
            if (publisher != ''):
                query +=  " AND LOWER(publisher) LIKE LOWER('%" + publisher + "%')"
                if (title != ''):
                    query += " AND LOWER(title) LIKE LOWER('%" + title + "%')"
                    if (subject != ''):
                        query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
                else:
                    if (subject != ''):
                        query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
            else:
                if (title != ''):
                    query += " AND LOWER(title) LIKE LOWER('%" + title + "%')"
                    if (subject != ''):
                        query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
                else:
                    if (subject != ''):
                        query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
        else:
            if (publisher != ''):
                query +=  " WHERE LOWER(publisher) LIKE LOWER('%"+publisher+"%')"
                if (title != ''):
                    query += " AND LOWER(title) LIKE LOWER('%" + title + "%')"
                    if (subject != ''):
                        query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
                else:
                    if (subject != ''):
                        query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
            else:
                if (title != ''):
                    query += " WHERE LOWER(title) LIKE LOWER('%" + title + "%')"
                    if (subject != ''):
                        query += " AND LOWER(subject) LIKE LOWER('%" + subject + "%')"
                else:
                    if (subject != ''):
                        query += " WHERE LOWER(subject) LIKE LOWER('%" + subject + "%')"
        query += " GROUP BY Books.ISBN"
        if sortBy == 'year':
            query += " ORDER BY year"
            if Desc_Asc == 'd':
                query += " Desc"
        elif sortBy == 'score':
            query += " ORDER BY score"
            if Desc_Asc == 'd':
                query += ' Desc'
        else:
            pass

        try:
            print(query)
            db = dbconnect.dbConnect()
            results = db.readDB(query)
            return results
        except Exception as ex:
            print ex.message

    def searchISBN(self, ISBN):
        query = "SELECT * " \
                "FROM Books " \
                "WHERE ISBN = " + "'" + ISBN + "';"
        try:
            db = dbconnect.dbConnect()
            results = db.readDB(query)
            return results
        except Exception as ex:
            print ex.message

    #Function 9: Useful feedbacks
    def feedBackRank(self, ISBN, n):
        query = "SELECT Rate.feedback_name, Feedbacks.text, Feedbacks.score, AVG(usefulness), Feedbacks.date FROM Rate, Feedbacks \
                  WHERE Rate.feedback_name = Feedbacks.login_name AND Feedbacks.ISBN = Rate.ISBN AND Rate.ISBN = '" + ISBN + "' GROUP BY Rate.feedback_name ORDER BY AVG(Rate.usefulness) DESC LIMIT " + str(n)

        try:
            db = dbconnect.dbConnect()
            results = db.readDB(query)
            return results
        except Exception as ex:
            print ex.message

    #Function 10: Book recommendation

    def getRecommendation(self, ISBN, login_name):
        query = "SELECT ISBN, sum(copies) \
                FROM Orders, Items \
                WHERE Orders.oid = Items.oid \
                AND ISBN in (SELECT distinct ISBN \
                             FROM (SELECT distinct login_name \
                                    FROM Orders, Items \
                                    WHERE Orders.oid = Items.oid  \
                                    AND ISBN = '" + ISBN + "') C, Orders O, Items I \
                               WHERE c.login_name = o.login_name \
                                AND O.oid = I.oid) \
                AND Orders.login_name in (SELECT distinct login_name \
                                            FROM Orders, Items \
                                            WHERE Orders.oid = Items.oid  \
                                            AND ISBN = '" + ISBN + "') \
                AND ISBN not in (SELECT  ISBN   \
	             			FROM Orders, Items  \
	               			WHERE Orders.oid = Items.oid    \
	                    	AND login_name = '" + login_name + "') \
                GROUP BY ISBN \
                ORDER BY sum(copies) DESC"

        try:
            db = dbconnect.dbConnect()
            results = db.readDB(query)
            return results
        except Exception as ex:
            print ex.message


    #Function 11: Statistics
    # the list of the m most popular books (in terms of copies sold in this month)
    def popularBooks(self, m):
        year = datetime.date.today().year
        month = datetime.date.today().month

        query = "SELECT ISBN, SUM(copies) \
                    FROM (SELECT ISBN, copies \
                          FROM Orders JOIN Items on Orders.oid = Items.oid \
                          WHERE  MONTH(date) = " + str(month) + " AND YEAR(date) = " + str(year) + " AND status = 'Complete') info \
                    GROUP BY ISBN \
                    ORDER BY SUM(copies) DESC \
                    LIMIT " + str(m)

        try:
            db = dbconnect.dbConnect()
            results = db.readDB(query)
            return results
        except Exception as ex:
            print ex.message
    # the list of m most popular authors
    def popularAuthors(self, m):
        year = datetime.date.today().year
        month = datetime.date.today().month

        query = "SELECT authors, SUM(sale) \
                FROM (SELECT ISBN, SUM(copies) sale \
                      FROM (SELECT ISBN, copies \
                            FROM Orders o, Items i \
                            WHERE o.oid = i.oid AND MONTH(date) = " + str(month) + " AND YEAR(date) = " + str(year) + " AND status = 'Complete') info \
                      GROUP BY ISBN) sales, Books \
                WHERE sales.ISBN = Books.ISBN \
                GROUP BY authors \
                ORDER BY SUM(sale) DESC \
                LIMIT " + str(m)

        try:
            db = dbconnect.dbConnect()
            results = db.readDB(query)
            return results
        except Exception as ex:
            print ex.message


    # the list of m most popular publishers


    def popularPublishers(self, m):
        year = datetime.date.today().year
        month = datetime.date.today().month

        query = "SELECT publisher, SUM(sale) \
                FROM (SELECT ISBN, SUM(copies) sale \
                      FROM (SELECT ISBN, copies \
                            FROM Orders o, Items i \
                            WHERE o.oid = i.oid AND MONTH(date) = " + str(month) + " AND YEAR(date) = " + str(year) + " AND status = 'Complete') info \
                      GROUP BY ISBN) sales, Books \
                WHERE sales.ISBN = Books.ISBN \
                GROUP BY publisher \
                ORDER BY SUM(sale) DESC \
                LIMIT " + str(m)

        try:
            db = dbconnect.dbConnect()
            results = db.readDB(query)
            return results
        except Exception as ex:
            print ex.message