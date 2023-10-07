from typing import Optional
from pydantic import BaseModel
import datetime as _dt 
import sqlalchemy as _sql

import DB.database as _database


class Todo(_database.Base):
    __tablename__ = "todo"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, nullable=False, index=True)
    description = _sql.Column(_sql.String, nullable=True)
    finished = _sql.Column(_sql.Boolean, nullable=False)
