import secrets
from os import getenv
import database as db

class UndefinedCredentialsException(Exception):
    pass

class Authenticator:
    master_user: str | None
    master_passwd: str | None
    admins: dict[str, str] = {}

    def __init__(self):
        self.master_user = getenv("AUTH_USER")
        self.master_passwd = getenv("AUTH_PASS")

        for admin in db.get_admin_list(include_password=True):
            self.admins[admin.user] = admin.password

        if (self.master_user == None or self.master_passwd == None) and len(self.admins) == 0:
            raise UndefinedCredentialsException("Please set AUTH_USER and AUTH_PASS environment variables for defining the master user")

    def authenticate(self, user: str, password: str) -> bool:
        if self.master_user != None or self.master_passwd != None:
            passwd_is_correct = secrets.compare_digest(password, self.master_passwd)
            user_is_correct = secrets.compare_digest(user, self.master_user)

        else:
            user_passwd = self.admins.get(user)
            if user_passwd != None:
                user_is_correct = True
                passwd_is_correct = secrets.compare_digest(password, user_passwd)
        if user_is_correct and passwd_is_correct: return True
        else:                                     return False

    def refresh(self):
        self.admins = {}
        for admin in db.get_admin_list(include_password=True):
            self.admins[admin.user] = admin.password
