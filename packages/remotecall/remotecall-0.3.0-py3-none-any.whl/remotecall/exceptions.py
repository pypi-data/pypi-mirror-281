class ConnectionTimeoutError(ConnectionError):
    """Raised when a connection fails due a timeout error."""


class ConnectTimeoutError(ConnectionTimeoutError):
    """Failed to establishing a connection in given time.

    Use set_timeout(timeout) to set a proper timeout. Note that connect_timeout
    and read_timeout can be defined as a tuple (connect_timeout, read_timeout).
    """


class ConnectionReadTimeoutError(ConnectionTimeoutError):
    """Failed to read data from a connection within given time out.

    Use set_timeout(timeout) to set a proper timeout. Note that connect_timeout
    and read_timeout can be defined as a tuple (connect_timeout, read_timeout).
    """


class ClientError(Exception):
    """4xx: Client error"""

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ServerError(Exception):
    """5xx: Server error"""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
