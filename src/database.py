from sqlalchemy import create_engine, Column, Integer, String  
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
import config


sqlite_url = config.get_conf('SQLITE_DATABASE_URL')
sqlite_engine = create_engine(
            sqlite_url,
            **config.SQLALCHEMY_ENGINE_OPTIONS
        );

SqliteSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=sqlite_engine)

SqliteBase = declarative_base()


mysql_url = config.get_mysql_url()
mysql_engine = create_async_engine(
    mysql_url,echo=True
)
MysqlSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=mysql_engine, class_=AsyncSession)
MysqlBase = declarative_base()
