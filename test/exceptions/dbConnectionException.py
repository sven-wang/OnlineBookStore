class dbConnectionException(Exception):
    """Exception raised for errors in connecting with database.
    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        self.msg = msg