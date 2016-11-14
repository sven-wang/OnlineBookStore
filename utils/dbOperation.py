import dbconnect

class dbOperation:
    def registration(self, login_name, full_name, passwords, card_num, address, phone_num):
        query = "INSERT INTO Customers (login_name, full_name, passwords, card_num, address, phone_num) " \
                "VALUES ('"+login_name+"', '"+full_name+"', '"+passwords+"', '"+card_num+"', '"+address+"', '"+phone_num+"');"
        print query
        try:
            db = dbconnect.dbConnect()
            db.insertDB(query)
        except Exception as ex:
            print ex.message

