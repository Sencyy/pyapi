from enum import Enum
from pydantic import BaseModel
class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"


class User(BaseModel):
    id: int | None = None
    name: str
    age: int
    role: str
    salary: int
    gender: Gender

    def __repr__(self):
        return f"Usuário\n ID: {self.id}\n Nome: {self.name}\n Idade: {self.age}\n Sexo: {self.gender}\n Trabalho: {self.role}\n Salario: {self.salary}"

    def to_dict(self):
        return {
                "name": f"{self.name}",
                "age": f"{self.age}",
                "gender": "f{self.gender}",
                "role": f"{self.role}",
                "salary":f"{self.salary},"
                }

class Admin(BaseModel):
    id: int | None = None
    user: str
    password: str = "REDACTED"
    permission: str = "Admin"
