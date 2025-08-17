import secrets
from datetime import datetime, timedelta
class ApiKey():
    key: str
    expire_date: datetime

    def __init__(self, duration: timedelta):
        self.key = secrets.token_urlsafe(24)
        self.expire_date = datetime.now() + duration

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

    def generate_key(self, duration: timedelta) -> str:
        new_key = ApiKey(duration)
        self.store[new_key.key] = new_key
        return new_key.key
