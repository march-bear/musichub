class UserNotFoundException(Exception):
    pass

class ProjectNotFoundException(Exception):
    pass

class ProjectAlreadyExistsException(Exception):
    pass

class EmailAlreadyBusyException(Exception):
    pass

class UserBannedException(Exception):
    pass

class BadCredentialsException(Exception):
    pass
