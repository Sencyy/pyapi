import sqlite3
from hashlib import sha256
from users import User, Admin

class AdminNotFoundException(Exception):
    pass

ALLOWED_USER_PROPERTIES = {"name", "age", "gender", "role", "salary"}

def get_user_list():
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        ulist = []
        for row in rows:
            u = User(id=row[0], name=row[1], age=row[2], gender=row[3], role=row[4], salary=row[5])
            ulist.append(u)
            print(u)

        return ulist


def insert_user(user: User):
   with sqlite3.connect("database.db") as conn:
       cur = conn.cursor()

       cur.execute(
           "INSERT INTO users (name, age, gender, role, salary) VALUES (?, ?, ?, ?, ?)",
           (user.name, user.age, user.gender.value, user.role, user.salary),
       )

       return cur.lastrowid

def retrieve_user(id):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE id = ?", (id,))
        user = cur.fetchone()
        return User(id=user[0], name=user[1], age=user[2], gender=user[3], role=user[4], salary=user[5])

def remove_user(id: int):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id = ?", (id,))

def change_user(id: int, property: str, value):
    if property not in ALLOWED_USER_PROPERTIES:
        raise ValueError(f"Invalid user property: {property}")

    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()

        cur.execute(f"UPDATE users SET {property} = ? WHERE id = ?", (value, id))
        cur.execute(f"SELECT {property} FROM users WHERE id = ?", (id,))
        value = cur.fetchone()

        return { "id": id, property: value[0] }

def get_admin_list(include_password=False):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM admins")
        rows = cur.fetchall()
        admlist = []

        if include_password:
            for row in rows:
                admlist.append(Admin(user=row[1], password=row[2]))
        else:
            for row in rows:
                admlist.append(Admin(user=row[1]))
        return admlist

def insert_admin(admin: Admin):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO admins (user, password, permission) VALUES (?, ?, ?)",
            (admin.user, sha256(bytes(admin.password, "utf-8")).hexdigest(), admin.permission),
        )

        return cur.lastrowid

def retrieve_admin(user=None, id=None) -> Admin:
    if user != None:
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM admins WHERE user = ?", (user,))
            admin = cur.fetchone()
            return Admin(id=admin[0], user=admin[1], permission=admin[3])
    elif id != None:
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM admins WHERE id = ?", (id,))
            admin = cur.fetchone()
            return Admin(id=admin[0], user=admin[1], permission=admin[3])
    else:
        raise AdminNotFoundException("Key issuer not found in database!")

def remove_admin(username: str):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()

        cur.execute("DELETE FROM admins WHERE user = ?", (username,))