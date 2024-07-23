from sqlalchemy import create_engine, Column, Integer, String  
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
import config


sqlite_url = config.get_conf('SQLITE_DATABASE_URL')
engine = create_engine(
            sqlite_url,
            **config.SQLALCHEMY_ENGINE_OPTIONS
        );


SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)



Base = declarative_base()


def get_sqlite_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()