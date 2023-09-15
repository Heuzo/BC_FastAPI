from datetime import datetime
from hashlib import md5
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, OAuth2PasswordBearer

from fake_db import fake_users
from models import User
from utils import create_jwt_token, read_jwt_token

app = FastAPI()
security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/login')


@app.get('/items/')
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}


@app.get('/')
async def main_page(response: Response):
    now = datetime.now()  # Получаем текущую дату и время
    response.set_cookie(key='last_visit', value=str(now))  # Устанавливаем куку
    return FileResponse('Front/index.html')


@app.post('/api/register')
async def register(user: User, response: Response):
    hash_id = md5(user.user_name.encode()).hexdigest()
    hash_pass = md5(user.password.encode()).hexdigest()

    if hash_id not in fake_users:
        fake_users[hash_id] = {
            'user_name': f'{user.user_name}',
            'password': f'{hash_pass}',
        }
        claim = {'userId': f'{user.user_name}', 'role': 'usergit '}
        response.status_code = status.HTTP_201_CREATED
        response.set_cookie(key='access_token', value=create_jwt_token(claim))
        return fake_users[hash_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with that login already exists',
        )


@DeprecationWarning
@app.get('/protected_resource')
async def protected(response: Response, token: Annotated[str, Depends(oauth2_scheme)]):
    if read_jwt_token('userId') in fake_users:
        response.status_code = status.HTTP_200_OK
        return {'message': 'Access allowed'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials'
        )


@app.post('/api/login')
async def clelogin_page(
    user: User, response: Response, token: Annotated[str, Depends(oauth2_scheme)]
):
    # Рефреш токена при успешной аутентифицаии JWT
    if read_jwt_token(token, 'userId') == user.user_name:
        claim = read_jwt_token(token)
        response.set_cookie(key='access_token', value=create_jwt_token(claim))
        response.status_code = status.HTTP_200_OK
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials'
        )


# Роут для доступа к примонтированной к докер контейнеру папке
@app.get('/api/data')
async def recieve_data():
    return FileResponse('data/hello.html')


# Роуты овтечащие за раздачу файлов статики по запросу фронта


@app.get('/assets/{file_path:path}')
async def css_static(file_path: str):
    return FileResponse(f'Front/assets/{file_path}')


@app.get('/images/{file_path:path}')
async def images_static(file_path: str):
    return FileResponse(f'Front/images/{file_path}')
