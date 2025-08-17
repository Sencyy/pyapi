from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from users import User, Gender, Admin
import database as db
from keyhandler import KeyStore
from datetime import timedelta
from auth import Authenticator
from typing import Annotated

security = HTTPBasic()
auth = Authenticator()
keystore = KeyStore()
key_time = timedelta(minutes=10)
app = FastAPI()

invalid_key_response = JSONResponse(status_code=401, content="Invalid API key!")
invalid_credentials_response = JSONResponse(status_code=401, content="Invalid credentials!")


@app.get("/")
def read_root():
    return {"Name": "pyapi"}

@app.get("/authenticate")
def handle_key(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if auth.authenticate(credentials.username, credentials.password):
        return keystore.generate_key(key_time)
    else: return invalid_credentials_response

@app.get("/users")
def list_users(apikey: str):
    if keystore.validate(apikey):
        ulist = db.get_user_list()
        jlist = [item.dict() for item in ulist]
        return jlist
    else: return invalid_key_response

@app.post("/users/new", status_code=201)
def create_user(apikey: str, name: str, age: int, gender: Gender, role: str, salary: int):
    if keystore.validate(apikey):
        user = User(name=name, age=age, gender=gender, role=role, salary=salary)
        id = db.insert_user(user)

        return {
            'Success': True,
            'id': id,
        }
    else: return invalid_key_response


@app.get("/users/{id}")
def get_user(apikey: str, id: int):
    if keystore.validate(apikey):
        user = db.retrieve_user(id)
        return user.model_dump()
    else: return invalid_key_response

@app.delete("/users/{id}")
def delete_user(apikey: str, id: int):
    if keystore.validate(apikey):
        db.remove_user(id)
        return {
            "Success": True,
            "id": id,
        }
    else: return invalid_key_response

@app.put("/users/{id}")
def edit_user(apikey: str, id: int, name=None, age=None, gender=None, role=None, salary=None):
    if keystore.validate(apikey):
        changes = []

        if name  :     changes.append(db.change_user(id, 'name', name))
        if age   :     changes.append(db.change_user(id, 'age', age))
        if gender:     changes.append(db.change_user(id, 'gender', gender))
        if role  :     changes.append(db.change_user(id, 'role', role))
        if salary:     changes.append(db.change_user(id, 'salary', salary))

        return changes
    else: return invalid_key_response


@app.get("/admins")
def list_admins(apikey: str):
    if keystore.validate(apikey):
        admlist = db.get_admin_list()
        jlist = [item.dict() for item in admlist]
        return jlist
    else: return invalid_key_response

@app.post("/admins/new")
def add_admin(apikey: str, user: str, password: str):
    if keystore.validate(apikey):
        id = db.insert_admin(Admin(user=user, password=password))
        auth.refresh()
        return {
            "Success": True,
            "id": id,
        }
    else: return invalid_key_response

@app.delete("/admins/{user}")
def delete_admin(apikey: str, user: str):
    if keystore.validate(apikey):
        db.remove_admin(user)
        auth.refresh()
        return {
            "Success": True,
            "username": user
        }
    else: return invalid_key_response
