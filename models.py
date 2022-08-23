from ast import Str
from re import S
from sqlalchemy import Column, Integer, String

from database import Base

class Books(Base):
    __tablename__ = "books" 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(String)
