import dbconnect

class dbOperation:
    #Fuction 1: Registration
    def registration(self, login_name, full_name, passwords, card_num, address, phone_num):
        query = "INSERT INTO Customers (login_name, full_name, passwords, card_num, address, phone_num) " \
                "VALUES ('"+login_name+"', '"+full_name+"', '"+passwords+"', '"+card_num+"', '"+address+"', '"+phone_num+"');"
        print query
        try:
            db = dbconnect.dbConnect()
            db.insertDB(query)
        except Exception as ex:
            print ex.message

    #Function 2: Ordering

    #Function 3: User Record
    def userRecord(self, login_name):
        # his/her account information
        query1 = "SELECT * " \
                 "FROM Customers " \
                 "WHERE login_name = " + "'" + login_name + "';"
        #query 2 =


        try:
            db = dbconnect.dbConnect()
            account_info = db.readDB(query1)
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
