from models import User
from fake_db import fake_users
from hashlib import md5
import jwt
from fastapi import status, HTTPException
from settings import SECRET_KEY, JWT_ALGORITHM


# Аутентификация на основании сверки хешей Логина / Пароля
def check_auth(user: User) -> bool: 
    rec_hash_id = md5(user.user_name.encode()).hexdigest()  # Хеш полученного имени (Для проверки, есть ли юзер в БД)
    rec_hash_pasword = md5(user.password.encode()).hexdigest()  # Хеш полученного пароля

    # Поиск ID пользователя в БД, в случае успеха произойдет проверка на соответствие хешей паролей
    if rec_hash_id in fake_users:
        if fake_users[rec_hash_id]:
            if fake_users[rec_hash_id]['password'] == rec_hash_pasword:
                return True
    return False


# Функция для создания JWT токена
def create_jwt_token(payload) -> str:
    encoded_jwt = jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)    # Кодируем токен
    return encoded_jwt


# Функция для чтения выбранного параметра ( заявки / claim )
def read_jwt_token(token: str, claim: str | None = None) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, JWT_ALGORITHM)     # Декодируем токен
        print(payload)
        print(payload.get(f'{claim}'))
        if claim == None:
            return payload
        return payload.get(f'{claim}')

    except jwt.ExpiredSignatureError:   # Обработка истекшего токена
        HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token is expired",
        )

    except jwt.InvalidTokenError:   # Обработка неверного токена
        HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token is invalid",
        )
