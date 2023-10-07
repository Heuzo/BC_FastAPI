from datetime import datetime, timedelta
from hashlib import md5

import jwt
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer

from DB.schemas import User
from fake_db import fake_users
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/login')


# Функция для получения пользовательских данных на основе имени пользователя
def get_user(username: str) -> User | None:
    if username in fake_users:
        user_data = fake_users[username]
        return User(**user_data)
    return None


# Аутентификация на основании сверки хешей Логина / Пароля
def check_auth(user: User) -> bool:
    rec_hash_id = md5(
        user.user_name.encode()
    ).hexdigest()  # Хеш полученного имени (Для проверки, есть ли юзер в БД)
    rec_hash_pasword = md5(user.password.encode()).hexdigest()  # Хеш полученного пароля
    # Поиск ID пользователя в БД и последующая сверка хешей паролей
    if rec_hash_id in fake_users:
        if fake_users[rec_hash_id]:
            if fake_users[rec_hash_id]['password'] == rec_hash_pasword:
                return True
    return False


# Функция для создания JWT токена
def create_jwt_token(payload: dict) -> str:
    body = payload.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES  # UTC.NOW + LifeTimeToken = Expiration
    )
    # Добавляем в токен парамтр срока жизни токена
    body.update({'exp': expire})
    # Кодируем токен
    encoded_jwt = jwt.encode(body, SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


# Проверка, пользовательских данных и генерация JWT токена
def auth_and_token(user: User, response: Response):
    # Проверяем есть ли пользователь в базе
    user_data_from_db = get_user(user.username)
    if (user_data_from_db is not None) and (
        user.password == user_data_from_db.password
    ):
        # Формируем заявки/claims/записи и заносим их в JWT body
        claims = {'sub': f'{user_data_from_db.username}'}
        if user_data_from_db.role == 'admin':
            claims['role'] = 'admin'
        else:
            claims['role'] = 'user'
        access_token = create_jwt_token(claims)
        response.status_code = status.HTTP_201_CREATED
        return {'access_token': access_token, 'token_type': 'bearer'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials'
        )


# Функция для проверки токена выбранного параметра ( заявки / claim )
def read_jwt_token(
    token: str = Depends(oauth2_scheme), claim: str | None = None
) -> str:
    print(f'Начало выполнения {read_jwt_token.__name__} \nToken: {token}')
    # Декодируем токен
    try:
        payload = jwt.decode(token, SECRET_KEY, JWT_ALGORITHM)
        if claim is None:
            print(payload)
            return payload
        else:
            print(payload.get(f'{claim}'))
            return payload.get(f'{claim}')

    # Обработка истекшего токена
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Token is expired'
        )

    # Обработка неверного токена
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Token is invalid'
        )


# Регистрация/добавление пользователя в базу
def register_user(user: User):
    # Получаем хеши ID/Пароля из JSON для дальнейшей обработки
    hash_id = md5(user.user_name.encode()).hexdigest()
    hash_pass = md5(user.password.encode()).hexdigest()

    # Если пользователя еще нет в системе - заносим в базу
    if hash_id not in fake_users:
        fake_users[hash_id] = {
            'username': f'{user.user_name}',
            'password': f'{hash_pass}',
        }

    # Иначе - выпуливаем эксепшен
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with that login already exists',
        )


def is_admin(token):
    if token['role'] == 'admin':
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not permitted resource'
        )
