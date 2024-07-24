from datetime import datetime,date
from enum import Enum
from typing import Optional,List

from fastapi import APIRouter, Query , Path,Body,Cookie , Header,HTTPException
from pydantic import BaseModel,Field
import goods.schemas as good_schemas
import goods.service as good_service
from sqlalchemy.ext.asyncio import AsyncSession
from goods.dependencies import get_mysql_db
from fastapi import Depends
import logging

logger = logging.getLogger(__name__)

good_router = APIRouter(prefix='/goods')


@good_router.post("/create",response_model=good_schemas.GoodVo)
async def create_good(good:good_schemas.Goods,db:AsyncSession= Depends(get_mysql_db)):
    try:
        db_good = await good_service.get_good_by_code(good.goood_code,db) 
        if db_good:
            raise HTTPException(status_code=400,detail=f"Goods [{good.goood_code}] already exists")
        return await good_service.create_good(good,db)
    except Exception as e:
        logger.error(f"good:{good.model_dump()}",e)
        raise HTTPException(status_code=400,detail=str(e))


@good_router.get("/get/{code}",response_model=good_schemas.GoodVo)
async def get_good(code:str,db:AsyncSession= Depends(get_mysql_db)):
    db_good = await good_service.get_good_by_code(code,db)
    if not db_good:
        raise HTTPException(status_code=404,detail=f"Good [{code}] not found")
    return db_good