class dbConnectionException(Exception):
    """Exception raised for errors in connecting with database.
    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        super(dbConnectionException, self).__init__(msg)
       # self.msg = msg


class dbInsertException(Exception):
    """Exception raised for errors when inserting into database.

    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        self.msg = msg


class dbUpdateException(Exception):
    """Exception raised for errors when updating data in database.

    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        self.msg = msg