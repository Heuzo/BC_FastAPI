import os
from hashlib import md5
from random import randbytes

SECRET_KEY = os.getenv('JWT_KEY', f'{md5(randbytes(128)).hexdigest()}')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
