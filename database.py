import sqlite3
from users import User, Admin

def get_user_list():
    conn = sqlite3.connect("database.db")
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
   conn = sqlite3.connect("database.db")
   cur = conn.cursor()

   cur.execute(f"INSERT INTO users (name, age, gender, role, salary) VALUES ('{user.name}', {user.age}, '{user.gender.value}', '{user.role}', {user.salary})")
   conn.commit()

   return cur.lastrowid

def retrieve_user(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM users WHERE id = {id}")
    user = cur.fetchone()
    return User(id=user[0], name=user[1], age=user[2], gender=user[3], role=user[4], salary=user[5])

def remove_user(id: int):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(f"DELETE FROM users WHERE id = {id}")
    conn.commit()

def change_user(id: int, property: str, value):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(f"UPDATE users SET {property} = '{value}' WHERE id = {id}")
    conn.commit()
    cur.execute(f"SELECT {property} FROM users WHERE id = {id}")
    value = cur.fetchone()

    return { "id": id, property: value[0] }

def get_admin_list(include_password=False):
    conn = sqlite3.connect("database.db")
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
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(f"INSERT INTO admins (user, password, permission) VALUES ('{admin.user}', '{admin.password}', '{admin.permission}')")
    conn.commit()

    return cur.lastrowid

def remove_admin(username: str):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(f"DELETE FROM users WHERE name = '{username}'")
    conn.commit()
