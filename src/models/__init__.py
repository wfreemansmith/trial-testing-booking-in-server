from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sessions(Base):
    __tablename__ = "sessions"
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    session_name = Column(String, nullable=False)
    session_start = Column(Date, nullable=False)
    session_end = Column(Date, nullable=False)
    session_upload_destination = Column(String)


def get_model_by_tablename(tablename: str):
    """Uses table name to return the relevant ORM model class"""
    for mapper in Base.registry.mappers:
        model = mapper.class_
        if hasattr(model, "__tablename__") and model.__tablename__ == tablename:
            return model
    return None
        

MAPPER = {
    "sessions": Sessions
}

# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Candidate(Base):
#     __tablename__ = 'candidates'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
