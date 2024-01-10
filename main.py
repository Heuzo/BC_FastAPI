from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List

from fastapi import Depends, FastAPI, Response, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm

from DB.tools import PostgresTools
from models.models import TodoModel

app = FastAPI(
    title='Heuzon API',
    description='Документация к сервису, реализованному в рамках обучения',
)
security = HTTPBasic()

if TYPE_CHECKING:
    pass


@app.on_event('startup')
def prepare_base():
    PostgresTools._add_tables()


@app.on_event('shutdown')
def clean_up_base():
    PostgresTools._drop_tables()


@app.get('/')
async def main_page(response: Response):
    # Получаем текущую дату и время
    now = datetime.now()
    # Устанавливаем куку
    response.set_cookie(key='last_visit', value=str(now))
    return FileResponse('Front/index.html')


# @app.post('/api/login', tags=['Auth'])
# async def login(
#     user: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
# ):
#     return auth_and_token(user, response)


# @app.get('/api/admin', tags=['Auth'])
# async def admin(token=Depends(read_jwt_token)):
#     if is_admin(token):
#         return {'Message': 'Success'}


# @app.get('/api/protected')
# async def protected(token=Depends(read_jwt_token)):
#     return {'message': 'Success'}


# ----------------- CRUD -------------------


@app.post('/api/todo', tags=['ToDo CRUD'], status_code=status.HTTP_201_CREATED)
async def create_todo(data: TodoModel):
    todo = PostgresTools.add_todo(data.title, data.description)
    return todo


@app.get('/api/todo', tags=['ToDo CRUD'])
async def get_all_todo():
    todos = PostgresTools.get_todo_all()
    return todos


@app.get('/api/todo/{todo_id}', tags=['ToDo CRUD'])
async def get_one_todo(todo_id: int):
    todo = PostgresTools.get_todo_by_id(id=todo_id)
    return todo


# TODO: Вынести логику обновления пользователя в сервисы
@app.put('/api/todo/{todo_id}')
async def update_todo(todo_id: int, data: TodoModel):
    todo = PostgresTools.update_todo_by_id(
        todo_id,
        title=data.title,
        description=data.description,
        completed=data.completed,
    )
    return todo


# TODO Вынести логику удаления пользователя в сервисы
@app.delete('/api/todo/{todo_id}', tags=['ToDo CRUD'])
async def delete_todo(todo_id: int):
    PostgresTools.delete_todo_by_id(todo_id)
    return {'message': 'Success'}


@app.delete('/api/todo', tags=['ToDo CRUD'])
async def delete_all_todo():
    PostgresTools.delete_all_todo()
    return {'message': 'Success'}


# ----------------- END OF CRUD -------------------


# Роуты овтечащие за раздачу файлов статики по запросу фронта
@app.get('/assets/{file_path:path}', tags=['Static'])
async def css_static(file_path: str):
    return FileResponse(f'Front/assets/{file_path}')


@app.get('/images/{file_path:path}', tags=['Static'])
async def images_static(file_path: str):
    return FileResponse(f'Front/images/{file_path}')
