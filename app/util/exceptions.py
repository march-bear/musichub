class NotFoundException(Exception):
    def __init__(self, entity: str, details: str | None = None):
        self.entity = entity
        self.details = details

class ProjectAlreadyExistsException(Exception):
    pass

class EmailAlreadyBusyException(Exception):
    pass

class UserBannedException(Exception):
    pass

class BadCredentialsException(Exception):
    pass

class InvalidConfirmationTokenException(Exception):
    pass

class EmailNotConfirmedException(Exception):
    pass
