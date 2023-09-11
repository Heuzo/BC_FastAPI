from models import User
from fake_db import fake_users
import uuid 
from hashlib import md5
import base64
import jwt 

def check_auth(user: User) -> bool: 
    rec_hash_id = md5(user.user_name.encode()).hexdigest()  # Хеш полученного имени (Для проверки, есть ли юзер в БД)
    rec_hash_pasword = md5(user.password.encode()).hexdigest()  # Хеш полученного пароля

    # Поиск ID пользлвателя в БД, в случае успеха произйдет проверка на соответствие хешей паролей
    if rec_hash_id in fake_users:
        if fake_users[rec_hash_id]:
            if fake_users[rec_hash_id]['password'] == rec_hash_pasword:
                return True
    return False

def generate_token(payload, secret, alg):
    encoded_jwt = jwt.encode(payload, secret, algorithm=alg)
    print(encoded_jwt)

generate_token({'name':'vlad'}, 'hello', alg="HS256")