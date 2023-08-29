from fastapi import FastAPI, Response, Form
from fastapi.responses import FileResponse
from enum import Enum
from pydantic import BaseModel
from models import CalculateData, User, FeedBack, UserCreate, LoginUser
from fake_db import fake_users, sample_products
from datetime import datetime
from data.data import data_json

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

@app.get("/api/user/{user_id}")
async def user_info(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}

@app.get("/api/data")
async def recieve_data():
    return FileResponse("data/hello.html")


@app.get("/assets/{file_path:path}")
async def css_static(file_path: str):
    return FileResponse(f"Front/assets/{file_path}")

@app.get("/images/{file_path:path}")
async def images_static(file_path: str):
    return FileResponse(f"Front/images/{file_path}")
