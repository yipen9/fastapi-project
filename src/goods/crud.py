from sqlalchemy.ext.asyncio import AsyncSession
from goods.models import GoodsDB
from goods.schemas import Goods
from sqlalchemy import select


async def get_good(db:AsyncSession,good_id:int):
    statement = select(GoodsDB).where(GoodsDB.id == good_id)
    result = await db.execute(statement)
    return result.scalars().first()


async def create_good(db:AsyncSession,good:Goods):
    goodDB = GoodsDB(good_name=good.good_name,good_code=good.goood_code,price=good.price)
    db.add(goodDB)
    await db.commit()
    await db.refresh(goodDB)
    return goodDB


async def get_good_by_code(db:AsyncSession,good_code:str):
    statement = select(GoodsDB).where(GoodsDB.good_code == good_code)
    result = await db.execute(statement)
    return result.scalars().first()