from fastapi import FastAPI, Response, Form, Cookie
from fastapi.responses import FileResponse
from enum import Enum
from pydantic import BaseModel
from models import CalculateData, User, FeedBack, UserCreate, LoginUser
from fake_db import fake_users, sample_products, sessions
from datetime import datetime
from typing import Annotated

app = FastAPI()


@app.get("/")
async def main_page(response: Response):
    now = datetime.now()    # Получаем текущую дату и время
    return FileResponse('Front/index.html')

@app.get("/login")
async def login_page():
    return FileResponse('Front/login.html')

@app.post("/api/login")
async def login(login: Annotated[str, Form()], password: Annotated[str, Form()], response: Response):
    session_id = 'SID' + str(hash(login + password))
    sessions[session_id] = {'username': f'{login}', 'password': f'{password}'}
    response.set_cookie(key='session_token', value=f'{session_id}', httponly=True)
    return sessions


@app.post("/api/user")
async def user(response: Response, session_token: str | None = Cookie(default=None)):
    if session_token:
        if session_token and session_token in sessions:
            return sessions[session_token]
        else:
            response.status_code = 401
            return {"message": "Unauthorized"}

    

@app.post("/api/calculate")
async def calculate_sum(data: CalculateData):
    return {'result': data.num1 + data.num2}


@app.post("/api/feedback")
async def feedback(data: FeedBack):
    return {"message": f"Feedback recieved. Thank you, {data.name}"}

@app.post("/api/create_user")
async def create_user(user: UserCreate):
    return user

@app.get("/api/product/{product_id}")
async def product_info(product_id: int):
    for product in sample_products:
        if product.get('product_id') == product_id:
            return product

@app.get("/api/products/search")
async def product_search(keyword: str, category: str = None, limit: int = 10):
    new_array = []
    for dictionary in sample_products:
        for key in dictionary:
            if keyword in str(dictionary[key]):
                if category:
                    if category == dictionary.get('category'):
                        new_array.append(dictionary)
                else:
                    new_array.append(dictionary)
    return new_array

@app.get("/assets/{file_path:path}")
async def css_static(file_path: str):
    return FileResponse(f"Front/assets/{file_path}")

@app.get("/images/{file_path:path}")
async def images_static(file_path: str):
    return FileResponse(f"Front/images/{file_path}")
