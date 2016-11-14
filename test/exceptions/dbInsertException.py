class dbInsertException(Exception):
    """Exception raised for errors when inserting into database.

    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        self.msg = msg