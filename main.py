from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm

from utils import oauth2_scheme, read_jwt_token, auth_and_token, is_admin


app = FastAPI()
security = HTTPBasic()



@app.get('/items/')
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}


@app.get('/')
async def main_page(response: Response):
    # Получаем текущую дату и время
    now = datetime.now()
    # Устанавливаем куку
    response.set_cookie(key='last_visit', value=str(now))
    return FileResponse('Front/index.html')


@app.post('/api/login')
async def authentification(user: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    return auth_and_token(user, response)


@app.get('/api/admin')
async def admin(token = Depends(read_jwt_token)):
    if is_admin(token):
        return {'Message': 'Success'}



@app.get('/api/protected')
async def protected(token = Depends(read_jwt_token)):
    return {'message': 'Success'}


# Роут для доступа к примонтированной к докер контейнеру папке
@app.get('/api/data')
async def recieve_data(token = Depends(read_jwt_token)):
    return FileResponse('data/hello.html')



# Роуты овтечащие за раздачу файлов статики по запросу фронта

@app.get('/assets/{file_path:path}')
async def css_static(file_path: str):
    return FileResponse(f'Front/assets/{file_path}')


@app.get('/images/{file_path:path}')
async def images_static(file_path: str):
    return FileResponse(f'Front/images/{file_path}')
