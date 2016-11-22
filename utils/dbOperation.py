import dbconnect

class dbOperation:
    #Basic queries
    def get_max(self, table, sort_key):
        query = "SELECT "+sort_key+" " \
                "FROM "+table+" " \
                "ORDER BY "+sort_key+" DESC " \
                "LIMIT 1"
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

    #Function 2: Ordering
    #def ordering(self, login_name, date, status):



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


    #Function 7: Usefulness ratings

    #Function 8: Book Browsing
    

    #Function 9: Useful feedbacks

    #Function 10: Book recommendation

    #Function 11: Statistics
