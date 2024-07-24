import base_import as base_import
import config
import asyncio
from database import sqlite_engine,SqliteBase,mysql_engine,MysqlBase
from auth.models import UserDB
from goods.models import GoodsDB

# SqliteBase.metadata.create_all(bind=sqlite_engine)


async def create_mysql_tables():
    async with mysql_engine.begin() as conn:
        await conn.run_sync(MysqlBase.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_mysql_tables())