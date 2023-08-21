from fastapi import FastAPI, Response, Form
from fastapi.responses import FileResponse
from enum import Enum
from pydantic import BaseModel
from models import CalculateData, User, FeedBack, UserCreate, LoginUser
from fake_db import fake_users, sample_products
from datetime import datetime


app = FastAPI()


@app.get("/")
async def main_page(response: Response):
    now = datetime.now()    # Получаем текущую дату и время
    response.set_cookie(key="last_visit", value=now)    # Устанавливаем куку 
    return FileResponse('Front/index.html')

@app.get("/login")
async def login_page():
    return FileResponse('Front/login.html')

@app.post("/login")
async def login_page(user: LoginUser):
    return f'Данные пришли {user}'
    

@app.post("/api/calculate")
async def calculate_sum(data: CalculateData):
    return {'result': data.num1 + data.num2}


@app.post("/api/user")
async def is_adult(user: User):
    json = user.model_dump()
    if user.age >= 18:
        json.update({"is_adult": True})
    else:
        json.update({"is_adult": False})
    return json


@app.get("/api/user/{user_id}")
async def user_info(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


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
