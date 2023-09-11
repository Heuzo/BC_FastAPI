from pydantic import BaseModel


class CalculateData(BaseModel):
    num1: int
    num2: int


class ResultCalculate(BaseModel):
    result: int


class FeedBack(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: bool


class LoginUser(BaseModel):
    login: str
    passwod: str


class User(BaseModel):
    user_name: str
    password: str
