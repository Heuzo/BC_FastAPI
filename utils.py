from datetime import datetime, timedelta
from hashlib import md5

import jwt
from fastapi import HTTPException, status

from fake_db import fake_users
from models import User
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, SECRET_KEY


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
    body.update({'exp': expire})  # Добавляем в токен парамтр срока жизни токена
    encoded_jwt = jwt.encode(body, SECRET_KEY, JWT_ALGORITHM)  # Кодируем токен
    return encoded_jwt


# Функция для чтения выбранного параметра ( заявки / claim )
def read_jwt_token(token: str, claim: str | None = None) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, JWT_ALGORITHM)  # Декодируем токен
        print(payload)
        print(payload.get(f'{claim}'))
        if claim is None:
            return payload
        return payload.get(f'{claim}')

    except jwt.ExpiredSignatureError:  # Обработка истекшего токена
        HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token is expired')

    except jwt.InvalidTokenError:  # Обработка неверного токена
        HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token is invalid')


def register_user(user: User):
    # Получаем хеши ID/Пароля из JSON для дальнейшей обработки
    hash_id = md5(user.user_name.encode()).hexdigest()
    hash_pass = md5(user.password.encode()).hexdigest()

    # Если пользователя еще нет в системе - заносим в базу
    if hash_id not in fake_users:
        fake_users[hash_id] = {
            'user_name': f'{user.user_name}',
            'password': f'{hash_pass}',
        }

    # Иначе - выпуливаем эксепшен
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with that login already exists',
        )
