from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List

import sqlalchemy.orm as _orm
from fastapi import Depends, FastAPI, Response, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm

import DB.models as models
import DB.schemas as schemas
import DB.services as services
from utils import auth_and_token, is_admin, oauth2_scheme, read_jwt_token

app = FastAPI(title='Heuzon API', description='Документация к сервису, реализованному в рамках обучения')
security = HTTPBasic()


if TYPE_CHECKING:
    pass

@app.on_event('startup')
def prepare_base():
    services._add_tables()

@app.on_event('shutdown')
def clean_up_base():
    services._drop_tables()

@app.get('/')
async def main_page(response: Response):
    # Получаем текущую дату и время
    now = datetime.now()
    # Устанавливаем куку
    response.set_cookie(key='last_visit', value=str(now))
    return FileResponse('Front/index.html')

@app.post('/api/login',  tags=['Auth'])
async def login(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
):
    return auth_and_token(user, response)


@app.get('/api/admin', tags=['Auth'])
async def admin(token=Depends(read_jwt_token)):
    if is_admin(token):
        return {'Message': 'Success'}


@app.get('/api/protected')
async def protected(token=Depends(read_jwt_token)):
    return {'message': 'Success'}


# ----------------- CRUD ------------------- 

@app.post('/api/todo', response_model=schemas.Todo, tags=['ToDo CRUD'])
async def create_todo(
    todo: schemas.CreateTodo, db: _orm.Session = Depends(services.get_db)
    ):
    return await services.create_todo(todo=todo, db=db)

@app.get('/api/todo', response_model=List[schemas.Todo], tags=['ToDo CRUD'])
async def get_all_todo(db: _orm.Session = Depends(services.get_db)):
    return await services.get_all_todos(db=db)

@app.get('/api/todo/{todo_id}', response_model=schemas.Todo, tags=['ToDo CRUD'])
async def get_todo(todo_id: int, db: _orm.Session = Depends(services.get_db)):
    return await services.get_one_todo(db=db, todo_id=todo_id)

#TODO Вынести логику удаления пользователя из базы в сервисы
@app.delete('/api/todo/{todo_id}', tags=['ToDo CRUD'])
async def delete_todo(todo_id: int, db: _orm.Session = Depends(services.get_db)):
    todo = await services.get_one_todo(db=db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    
    await services.delete_one_todo(todo, db=db)
    return {'message': 'Success'}

@app.delete('/api/todo', tags=['ToDo CRUD'])
async def delete_todo(db: _orm.Session = Depends(services.get_db)):
    await services.delete_all_todo(db=db)
    return {'message': 'Success'}

# ----------------- END OF CRUD ------------------- 


# Роуты овтечащие за раздачу файлов статики по запросу фронта
@app.get('/assets/{file_path:path}', tags=['Static'])
async def css_static(file_path: str):
    return FileResponse(f'Front/assets/{file_path}')

@app.get('/images/{file_path:path}', tags=['Static'])
async def images_static(file_path: str):
    return FileResponse(f'Front/images/{file_path}')
