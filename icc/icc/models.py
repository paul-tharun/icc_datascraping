from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DATE, String, Integer
from uuid import uuid4
from icc import settings

DeclarativeBase = declarative_base()


def db_connect() -> Engine:
    """
    Creates database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_items_table(engine: Engine):
    """
    Create the Items table
    """
    DeclarativeBase.metadata.create_all(engine)


class playersData(DeclarativeBase):
    """
    Defines the items model
    """

    __tablename__ = "playersData"
    Name = Column("name", String)
    Country = Column("country", String)
    Type = Column("type", String)
    Date = Column("date", DATE)
    Rating = Column("rating", Integer)
    id = Column(String, primary_key=True, default=uuid4)
