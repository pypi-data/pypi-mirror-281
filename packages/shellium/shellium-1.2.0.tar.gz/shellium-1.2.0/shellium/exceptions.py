class ShelliumException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UserDataExistsError(ShelliumException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UserDataMakeError(ShelliumException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ShellDriverAlreadyRunningError(ShelliumException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ShellDriverVersionError(ShelliumException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
