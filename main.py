from fastapi import FastAPI, Response, status, HTTPException, Cookie
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic
from models import User
from datetime import datetime
from utils import check_auth, create_jwt_token, read_jwt_token
from fake_db import fake_users
from hashlib import md5
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBasic()


@app.get("/")
async def main_page(response: Response):
    now = datetime.now()    # Получаем текущую дату и время
    response.set_cookie(key="last_visit", value=str(now))    # Устанавливаем куку
    return FileResponse('Front/index.html')


@app.post("/api/register")
async def login_page(user: User, response: Response):
    hash_id = md5(user.user_name.encode()).hexdigest()
    hash_pass = md5(user.password.encode()).hexdigest()

    if hash_id not in fake_users:
        fake_users[hash_id] = {
            'user_name': f'{user.user_name}',
            'password': f'{hash_pass}'
            }
        claim = {'userId': f'{user.user_name}', 'role': 'user'}
        response.status_code = status.HTTP_201_CREATED
        response.set_cookie(key='access_token', value=create_jwt_token(claim))
        return fake_users[hash_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that login already exists"
        )


@app.get("/protected_resource")
async def protected(response: Response, access_token: str | None = Cookie(default=None)):
    if read_jwt_token('userId') in fake_users:
        response.status_code = status.HTTP_200_OK
        return {'message': 'Access allowed'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@app.post("/api/login")
async def login_page(user: User, response: Response, access_token: str | None = Cookie(default=None)):

    # Рефреш токена при успешной аутентифицаии JWT
    if read_jwt_token(access_token, 'userId') == user.user_name:
        claim = read_jwt_token(access_token)
        response.set_cookie(key='access_token', value=create_jwt_token(claim))
        response.status_code = status.HTTP_200_OK
        return access_token
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
