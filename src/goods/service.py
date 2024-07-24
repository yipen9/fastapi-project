# module specific business logic
from sqlalchemy.ext.asyncio import AsyncSession
from goods.models import GoodsDB
from goods.schemas import Goods
import goods.crud as good_crud 


async def create_good(good:Goods,db:AsyncSession):
    goodDB =  await good_crud.create_good(db,good)
    return goodDB
    

async def get_good_by_id(id:int,db:AsyncSession):
    good = await good_crud.get_good(db,id)
    return good

async def get_good_by_code(good_code:str,db:AsyncSession):
    good = await good_crud.get_good_by_code(db,good_code)
    return good