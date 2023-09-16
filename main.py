from datetime import datetime
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, OAuth2PasswordBearer

from fake_db import fake_users
from models import User
from settings import JWT_ALGORITHM, SECRET_KEY
from utils import create_jwt_token

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


@app.post('/api/login')
async def authentification(user: User, response: Response):
    # Проверяем есть ли пользователь в базе
    if user.user_name in fake_users:
        # Формируем заявки/claims/записи и заносим их в JWT body
        claims = {'userId': f'{user.user_name}', 'role': 'usergit '}
        access_token = create_jwt_token(claims)
        response.status_code = status.HTTP_201_CREATED
        return {'access_token': access_token, 'token_type': 'bearer'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials'
        )


@DeprecationWarning
@app.get('/protected_resource')
async def protected(response: Response, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Invalid token')
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail='Token has expired',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from None
    except jwt.DecodeError:
        raise HTTPException(
            status_code=401,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from None


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
