 # db models
from database import engine,Base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text



# SQLAlchemy ORM 模型  
class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column(Text,nullable=False,index=True)
    age = Column(Integer,nullable=False,index=False)
    hashed_password = Column(Text,nullable=False,index=False)
    email = Column(Text,nullable=False,index=True)
    favorite_band = Column(Text,nullable=True,index=False)
    website = Column(Text,nullable=True,index=False)
    created = Column(Text,nullable=False,index=False)