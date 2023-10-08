import os
from configparser import ConfigParser
from hashlib import md5
from random import randbytes

SECRET_KEY = os.getenv('JWT_KEY', f'{md5(randbytes(128)).hexdigest()}')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def config_db(filename='database.ini', section='postgresql'):
    # Создаем объект парсера
    parser = ConfigParser()

    # Читаем файл
    parser.read(filename)

    # Получаем секцию postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename)
        )
    return db
