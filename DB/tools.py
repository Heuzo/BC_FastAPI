import os 

from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = 'postgresql://myuser:password@localhost:5432/fastapi_database'

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)


class PostgresTools:
    session = sessionmaker(autoflush=False, bind=engine)


    @classmethod
    def add_todo(cls, title, description):
        todo = Todo(title=title, description=description)
        with cls.session(autoflush=False, bind=engine) as db:
            db.add(todo)
            db.commit()
            todo = db.query(Todo).get(todo.id)
        return todo
    

    @classmethod
    def get_todo_by_id(cls, id):
        with cls.session(autoflush=False, bind=engine) as db:
            todo = db.query(Todo).get(id)
        return todo
    

    @classmethod
    def get_todo_all(cls):
        with cls.session(autoflush=False, bind=engine) as db:
            all_todos = db.query(Todo).all()
        return all_todos


    @classmethod
    def delete_todo_by_id(cls, id):
        with cls.session(autoflush=False, bind=engine) as db:
            todo = db.query(Todo).get(id)
            if todo:
                db.delete(todo)
                db.commit()
                return True
    
    
    @classmethod
    def delete_all_todo(cls):
        with cls.session(autoflush=False, bind=engine) as db:
            todos = db.query(Todo).all()
            if todos:
                for item in todos:
                    db.delete(item)
                    db.commit()
            return True

    @classmethod
    def update_todo_by_id(cls, id, title, description, completed):
        with cls.session(autoflush=False, bind=engine) as db:
            todo = db.query(Todo).get(id)
            todo.title = title
            todo.description = description
            todo.completed = completed
            db.commit()
            todo = db.query(Todo).get(todo.id)
        return todo


    @staticmethod
    # Создать таблицы из всех моделей
    def _add_tables():
        return Base.metadata.create_all(bind=engine)


    @staticmethod
    # Удалить все сущетсвующие таблицы
    def _drop_tables():
        return Base.metadata.drop_all(bind=engine)

