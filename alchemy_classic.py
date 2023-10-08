from sqlalchemy import Boolean, Column, Integer, MetaData, String, Table, create_engine

# Метадата - информация о данных в ДБ
meta = MetaData()

# Создаем таблицы
todo = Table(
    'todo',
    meta,
    Column('id', Integer, primary_key=True),
    Column('title', String(30), nullable=False),
    Column('description', String(200), nullable=False),
    Column('completed', Boolean, nullable=False),
)


# Подключаемся к БД и заносим данные | субд+driver://login_db:password_db@host:port/name_db
engine = create_engine(
    'postgresql+psycopg2://postgres:vivaldi2101@127.0.0.1:5432/fastapi', echo=True
)
meta.create_all(engine)  # или todo.create(engine)

conn = engine.connect()

select_todo_all = todo.select()
insert_todo_query = todo.insert().values(
    title='Hello from alchemy', description='Alchemy description', completed=True
)
conn.execute(insert_todo_query)
result = conn.execute(select_todo_all)
conn.commit()


for row in result:
    print(f'Строка {row}')
