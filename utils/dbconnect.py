import MySQLdb
import config
#from exceptions import dbInsertException, dbUpdateException, dbConnectionException


class dbConnect(object):
    db = None

    def __init__(self):
        try:
            # Open database connection
            self.db = MySQLdb.connect("localhost", config.USERNAME, config.PASSWORD, config.SCHEMA)
        except Exception as ex:
            raise Exception("Fail to connect to database: "+ex.__str__())

    def readDB(self, query):
        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        # Execute the SQL command
        cursor.execute(query)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        return results

    def updateDB(self, query):
        try:
            # prepare a cursor object using cursor() method
            cursor = self.db.cursor()
            # Execute the SQL command
            cursor.execute(query)
            # Commit your changes in the database
            self.db.commit()
            return 1
        except Exception as ex:
            # Rollback in case there is any error
            self.db.rollback()
            raise Exception("Unable to execute database update: "+ex.__str__())

    def insertDB(self, query):
        try:
            # prepare a cursor object using cursor() method
            cursor = self.db.cursor()
            # Execute the SQL command
            cursor.execute(query)
            # Commit your changes in the database
            self.db.commit()
            return 1
        except Exception as ex:
            # Rollback in case there is any error
            self.db.rollback()
            raise Exception("Unable to inset to database: "+ex.__str__())
