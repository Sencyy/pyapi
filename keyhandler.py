import secrets
import database as db
from datetime import datetime, timedelta
from users import Admin
class ApiKey():
    key: str
    issuer: Admin
    expire_date: datetime

    def __init__(self, duration: timedelta, issuer: Admin):
        self.key = secrets.token_urlsafe(24)
        self.expire_date = datetime.now() + duration
        self.issuer = issuer

    def is_valid(self) -> bool:
        if datetime.now() >= self.expire_date:
            return False
        else:
            return True

class KeyStore:
    store: dict[str, ApiKey]

    def __init__(self):
        self.store = {}

    def validate(self, key: str) -> bool:
        select_key = self.store.get(key)
        if select_key != None:
            return select_key.is_valid()
        else:
            return False

    def generate_key(self, duration: timedelta, issuer: str) -> str:
        key_issuer = db.retrieve_admin(user=issuer)
        new_key = ApiKey(duration, key_issuer)
        self.store[new_key.key] = new_key
        return new_key.key

    def issuer(self, key: str):
        return self.store.get(key).issuer.user
