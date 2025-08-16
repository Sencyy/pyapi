from fastapi import FastAPI
from users import User, Gender
import database as db

app = FastAPI()

@app.get("/")
def read_root():
    return {"Name": "pyapi"}

@app.get("/users")
def list_users():
    ulist = db.get_user_list()
    jlist = [item.dict() for item in ulist]
    return jlist

@app.post("/users/new", status_code=201)
def create_user(name: str, age: int, gender: Gender, role: str, salary: int):
    user = User(name=name, age=age, gender=gender, role=role, salary=salary)
    id = db.insert_user(user)

    return {
        'Success': True,
        'id': id,
    }

@app.get("/user/{id}")
def get_user(id: int):
    user = db.retrieve_user(id)
    return user.model_dump()

@app.delete("/user/{id}")
def delete_user(id: int):
    db.remove_user(id)
    return {
        "Success": True,
        "id": id,
    }
