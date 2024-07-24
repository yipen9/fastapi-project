from database import MysqlSessionLocal

async def get_mysql_db():
    async with MysqlSessionLocal() as session:
        yield session