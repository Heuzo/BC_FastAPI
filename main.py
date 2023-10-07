from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List

import sqlalchemy.orm as _orm
from fastapi import Depends, FastAPI, Response, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm

import DB.schemas as schemas
import DB.services as services
from utils import auth_and_token, is_admin, oauth2_scheme, read_jwt_token

app = FastAPI()
security = HTTPBasic()


if TYPE_CHECKING:
    pass


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
async def authentification(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
):
    return auth_and_token(user, response)


@app.get('/api/admin')
async def admin(token=Depends(read_jwt_token)):
    if is_admin(token):
        return {'Message': 'Success'}


@app.get('/api/protected')
async def protected(token=Depends(read_jwt_token)):
    return {'message': 'Success'}


# ----------------- CRUD ------------------- 

@app.post('/api/todo', response_model=schemas.Todo)
async def create_todo(
    todo: schemas.CreateTodo, db: _orm.Session = Depends(services.get_db)
    ):
    return await services.create_todo(todo=todo, db=db)

@app.get('/api/todo', response_model=List[schemas.Todo])
async def get_all_todo(db: _orm.Session = Depends(services.get_db)):
    return await services.get_all_todos(db=db)

@app.get('/api/todo/{todo_id}', response_model=schemas.Todo)
async def get_todo(todo_id: int, db: _orm.Session = Depends(services.get_db)):
    return await services.get_one_todo(db=db, todo_id=todo_id)

@app.delete('/api/todo/{todo_id}')
async def delete_todo(todo_id: int, db: _orm.Session = Depends(services.get_db)):
    todo = await services.get_one_todo(db=db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    
    await services.delete_todo(todo, db=db)
    return {'message': 'Success'}

@app.patch('/api/db')
async def create_table():
    services._add_tables()
    return {'Message': 'Success'}

# ----------------- END OF CRUD ------------------- 


# Роуты овтечащие за раздачу файлов статики по запросу фронта
@app.get('/assets/{file_path:path}')
async def css_static(file_path: str):
    return FileResponse(f'Front/assets/{file_path}')

@app.get('/images/{file_path:path}')
async def images_static(file_path: str):
    return FileResponse(f'Front/images/{file_path}')
