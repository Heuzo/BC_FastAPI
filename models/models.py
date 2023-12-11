from pydantic import BaseModel
from typing import Union


class TodoModel(BaseModel):
    title: str
    description: str
    completed: Union[bool, None] = None