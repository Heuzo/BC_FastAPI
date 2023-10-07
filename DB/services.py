from . import database
from . import models
from . import schemas


def _add_tables():
    return database.Base.metadata.create_all(bind=database.engine)

def _add_todo():
    pass

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_todo(todo: schemas.CreateTodo, db: "Session") -> schemas.Todo:
    todo = models.Todo(**todo)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return schemas.Todo.from_orm(todo)