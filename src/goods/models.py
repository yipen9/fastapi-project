 # db models
from database import MysqlBase
from sqlalchemy import Column, Integer, VARCHAR,BigInteger,CHAR,Float,TIMESTAMP
from sqlalchemy.sql import func,text

# SQLAlchemy ORM 模型 
class GoodsDB(MysqlBase):
    __tablename__ = 'goods'
    id = Column(BigInteger, primary_key=True, index=True,autoincrement=True)
    good_code = Column(CHAR(10),nullable=False,index=True)
    good_name = Column(VARCHAR(128),nullable=False,index=False)
    price = Column(Float,nullable=False,index=False)
    created = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'),nullable=False,index=False)