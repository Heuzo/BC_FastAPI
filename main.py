from fastapi import FastAPI, Response, Form, Depends, status, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from enum import Enum
from pydantic import BaseModel
from models import CalculateData, User, FeedBack, UserCreate, LoginUser
from datetime import datetime
from fake_db import USER_DATA

app = FastAPI()
security = HTTPBasic()




# Симуляционный пример получения инфы о пользователе
def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


# Аутентификация
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials", 
                headers={"WWW-Authenticate": "Basic"}, # Заголовок в ответе нужен чтобы браузер повторно отобразил окно ввода данных
                )
    return user


@app.get("/")
async def main_page(response: Response):
    now = datetime.now()    # Получаем текущую дату и время
    response.set_cookie(key="last_visit", value=now)    # Устанавливаем куку 
    return FileResponse('Front/index.html')


@app.get("/protected/")
def get_protected_resource(user: User = Depends(authenticate_user)):
    return {}


@app.get("/login")
async def login_page(user: User = Depends(authenticate_user)):
    return {"message": "You got my secret, welcome"}


@app.post("/login")
async def login_page(user: User = Depends(authenticate_user)):
    return f'Данные пришли {user}'


@app.get("/api/data")
async def recieve_data():
    return FileResponse("data/hello.html")



# Роуты овтечащие за раздачу файлов статики по запросу фронта

@app.get("/assets/{file_path:path}")
async def css_static(file_path: str):
    return FileResponse(f"Front/assets/{file_path}")

@app.get("/images/{file_path:path}")
async def images_static(file_path: str):
    return FileResponse(f"Front/images/{file_path}")
