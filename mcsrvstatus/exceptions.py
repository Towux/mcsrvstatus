"""Exceptions for mcsrvstatus library."""


class MCSrvStatError(Exception):
    """Base exception for all library errors."""
    pass


class ServerNotFoundError(MCSrvStatError):
    """Exception for when server is not found or offline."""
    pass


class APIError(MCSrvStatError):
    """Exception for API errors."""
    pass


class ConnectionError(MCSrvStatError):
    """Exception for connection errors."""
    pass
