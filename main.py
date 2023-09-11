from fastapi import FastAPI, Response, Form, Depends, status, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import User
from datetime import datetime
from utils import check_auth, generate_token
from fake_db import fake_users
from hashlib import md5

app = FastAPI()
security = HTTPBasic()


@app.get("/")
async def main_page(response: Response):
    now = datetime.now()    # Получаем текущую дату и время
    response.set_cookie(key="last_visit", value=now)    # Устанавливаем куку 
    return FileResponse('Front/index.html')

@app.post("/register")
async def login_page(user: User):
    hash_id = md5(user.user_name.encode())
    hash_pass = md5(user.password.encode())
    fake_users[hash_id.hexdigest()] = {
        'user_name': f'{user.user_name}', 
        'password': f'{hash_pass.hexdigest()}'
        }
    return fake_users

@app.post("/login")
async def login_page(user: User):
    if check_auth(user):
        generate_token()
        return {"message": "Success"}
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid credentials", 
        )

# Роут для доступа к примонтированной к докер контейнеру папке
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
