from typing import List

from fastapi import HTTPException
from sqlalchemy import orm

from . import database, models, schemas


# Создать таблицы из всех моделей
def _add_tables():
    return database.Base.metadata.create_all(bind=database.engine)


# Удалить все сущетсвующие таблицы
def _drop_tables():
    return database.Base.metadata.drop_all(bind=database.engine)


# Получение экземпляра сессии к БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создание записи
async def create_todo(todo: schemas.CreateTodo, db: orm.Session) -> schemas.Todo:
    todo = models.Todo(**todo.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return schemas.Todo.from_orm(todo)


# Поиск всех имеющитхся записей
async def get_all_todos(db: orm.Session, reusable: bool = False) -> List[schemas.Todo]:
    todos = db.query(models.Todo).all()
    if reusable:
        return list(todos)
    else:
        return list(map(schemas.Todo.from_orm, todos))


# Поиск одной записи по ID
async def get_one_todo(db: orm.Session, todo_id: int) -> schemas.Todo:
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    return todo


# Поиск удаление записи
async def delete_one_todo(todo, db: orm.Session):
    db.delete(todo)
    db.commit()


# Удаление всех записей таблицы ToDo
async def delete_all_todo(db: orm.Session):
    todos = await get_all_todos(db=db, reusable=True)
    if todos is None:
        raise HTTPException(status_code=404, detail='All ToDo`s already deleted')

    for item in todos:
        await delete_one_todo(item, db=db)

    return {'message': 'All ToDo raws deleted'}


async def update_todo(
    db: orm.Session, todo_data: schemas.CreateTodo, todo: models.Todo
):
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.finished = todo_data.finished

    db.commit()
    db.refresh(todo)

    return schemas.Todo.from_orm(todo)
