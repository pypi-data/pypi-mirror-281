class ErrorCode:
    aborted = 10
    already_exists = 6
    cancelled = 1
    data_loss = 15
    deadline_exceeded = 4
    failed_precondition = 9
    internal = 13
    invalid_argument = 3
    not_found = 5
    ok = 0
    out_of_range = 11
    permission_denied = 7
    resource_exhausted = 8
    unauthenticated = 16
    unavailable = 14
    unimplemented = 12
    unknown = 2


class ErrorException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"ErrorException: code:{self.code} - message:{self.message}"


class ErrorDetailException(ErrorException):
    def __init__(self, code: int = 0, message: str = "", details: str = ""):
        super().__init__(code, message)
        self.details = details

    def __str__(self):
        return f"ErrorException: code:{self.code} - message:{self.message}"


class DBException(ErrorException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"DBException: code:{self.code} - message:{self.message}"


class KeyException(ErrorException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"KeyException: code:{self.code} - message:{self.message}"


class AuthException(ErrorException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"AuthException: code:{self.code} - message:{self.message}"
