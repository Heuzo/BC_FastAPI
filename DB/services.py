from . import database, models, schemas
from typing import List
from sqlalchemy import orm

# Создать таблицы из всех моделей
def _add_tables():
    return database.Base.metadata.create_all(bind=database.engine)


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
async def get_all_todos(db: orm.Session) -> List[schemas.Todo]:
    todos = db.query(models.Todo).all()
    return list(map(schemas.Todo.from_orm, todos))

# Поиск одной записи по ID
async def get_one_todo(db: orm.Session, todo_id: int) -> schemas.Todo:
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    return todo

# Поиск удаление записи
async def delete_todo(todo, db: orm.Session):
    print(todo)
    db.delete(todo)
    db.commit()