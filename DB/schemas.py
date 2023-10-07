from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = None


class Todo(BaseModel):
    id: int
    title: str
    description: str
    finished: bool

    class Config:
        from_attributes = True

class CreateTodo(BaseModel):
    title: str
    description: Optional[str] = None
    finished: Optional[bool] = False
