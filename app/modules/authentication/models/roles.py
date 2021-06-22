import os
import sys
import inspect
from datetime import datetime
import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Sequence,VARCHAR,DateTime
from sqlalchemy.orm import relationship
from database.db import Base, engine



currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class roles(Base):
    __tablename__ = "roles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer,Sequence('user_id_seq'), primary_key=True)
    name = Column(VARCHAR(255))
    url = Column(VARCHAR(255))
    method = Column(VARCHAR(255))
    description = Column(VARCHAR(255), default="")
    created_at=Column(DateTime, default=datetime.now())
    updated_at=Column(DateTime, default=datetime.now())


metadata = sqlalchemy.MetaData()
metadata.create_all(engine)
