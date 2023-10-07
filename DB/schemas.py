from pydantic import BaseModel
from typing import Optional



class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = None


class Todo(BaseModel):
    id: int
    title: str
    description: str
    finished: bool


class CreateTodo(BaseModel):
    title:int
    description: Optional[str] = None
    