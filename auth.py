import secrets
from os import getenv

class UndefinedCredentialsException(Exception):
    pass

class Authenticator:
    user: str | None
    passwd: str | None

    def __init__(self):
        self.user = getenv("AUTH_USER")
        self.passwd = getenv("AUTH_PASS")

        if self.user == None or self.passwd == None:
            raise UndefinedCredentialsException("Please set AUTH_USER and AUTH_PASS environment variables for user authentication")

    def authenticate(self, user: str, password: str) -> bool:
        passwd_is_correct = secrets.compare_digest(password, self.passwd)
        user_is_correct = secrets.compare_digest(user, self.user)

        if user_is_correct and passwd_is_correct: return True
        else:                                     return False
