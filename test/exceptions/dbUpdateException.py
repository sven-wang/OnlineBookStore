class dbUpdateException(Exception):
    """Exception raised for errors when updating data in database.

    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        self.msg = msg