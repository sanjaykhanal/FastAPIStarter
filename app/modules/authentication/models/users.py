import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Sequence,VARCHAR,DateTime,String
from sqlalchemy.sql.schema import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database.db import Base, engine
import os
import sys
import inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(255), server_default='admin')
    name = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(255))
    signature = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_enabled = Column(Boolean, default=True)
    __table_args__ = (
        PrimaryKeyConstraint(
            id, name='users_pkey'),
        {})

metadata = sqlalchemy.MetaData()
metadata.create_all(engine)
