import dbconnect
import datetime

class dbOperation:
    #Basic queries
    def get_max(self, table, sort_key):
        query = "SELECT " + sort_key + " " \
                "FROM " + table + " " \
                "ORDER BY " + sort_key + " DESC " \
                "LIMIT 1;"
        try:
            db = dbconnect.dbConnect()
            return db.readDB(query)
        except Exception as ex:
            print ex.message

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

    def ordering(self, login_name, ISBN):
        # check curent order status
        query1 = "SELECT status " \
                 "FROM (SELECT status, oid " \
                        "FROM Orders " \
                        "WHERE login_name = '" + login_name + "') " \
                 "WHERE oid = MAX(oid)"
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
            if status == 'Complete':
                # get global max oid
                oid = db.readDB(query2)
                # allocate a new oid
                oid = str(long(oid) + 1)
                # insert a new order
                db.insertDB("INSERT INTO Orders(" + oid + ", '" + login_name + "', CURDATE(), 'Processing')")
                # insert a new item under this oid
                db.insertDB("INSERT INTO Items(" + oid + ", '" + ISBN + "', copies)")

            if status == 'Processing':
                # get user's current max id
                oid = db.readDB(query3)
                # insert new item
                db.insertDB("INSERT INTO Items(" + oid + ", '" + ISBN + "', copies)")
        except Exception as ex:
            print ex.message

    def checkOut(self, oid):
        ## oid : int

        query = "UPDATE Orders " \
                "SET status = 'Complete' AND date = CURDATE()"  + \
                "WHERE oid = " + str(oid) + ";"
        try:
            db = dbconnect.dbConnect()
            db.updateDB(query)
        except Exception as ex:
            print ex.message


    #Function 3: User Record
    def userRecord(self, login_name):
        # his/her account information
        query1 = "SELECT * " \
                 "FROM Customers " \
                 "WHERE login_name = " + "'" + login_name + "';"

        # his/her full history of orders
        query2 = "SELECT * " \
                 "FROM Orders " \
                 "WHERE login_name = " + "'" + login_name + "';"

        # his/her full history of feedbacks
        query3 = "SELECT * " \
                 "FROM Feedbacks " \
                 "WHERE login_name = " + "'" + login_name + "';"

        # the list of all the feedbacks he/she ranked with respect to usefulness
        query4 = "SELECT * " \
                 "FROM Feedback f, Rate r " \
                 "WHERE login_name = " + "'" + login_name + "' AND f.fid = r.fid;"

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
                "VALUES ('"+login_name+"', '"+ISBN+"', CURDATE()) , '"+score+"', "+text+"');"
        insertRate = "INSERT INTO Rate VALUES ('Nobody', " + login_name + ", '"+ISBN+"', 0 )"
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
    def search(self, authors, publisher, title, subject):
        authors = authors.strip()
        publisher = publisher.strip()
        title = title.strip()
        subject = subject.strip()

        query = "SELECT * " \
                "FROM Books" \

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

        try:
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
        query = "SELECT AVG(usefulness) " \
                "FROM Rate " \
                "GROUP BY " + "'" + ISBN + "'" + \
                "ORDER BY AVG(usefulness)" + " DESC " \
                "LIMIT " + str(n) + ";"
        try:
            db = dbconnect.dbConnect()
            results = db.readDB(query)
            return results
        except Exception as ex:
            print ex.message

    #Function 10: Book recommendation

    def getRecommendation(self, ISBN):
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
    def popularThisMonth(self, m):
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
    # the list of m most popular publishers