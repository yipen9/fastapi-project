from datetime import datetime,date
from enum import Enum
from typing import Optional,List

from fastapi import APIRouter, Query , Path,Body,Cookie , Header,HTTPException
from pydantic import BaseModel,Field
import auth.schemas as auth_schemas
import auth.service as auth_service
from database import get_sqlite_db
from sqlalchemy.orm import Session
from fastapi import Depends
import logging

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix='/auth')


@auth_router.post("/create",response_model=auth_schemas.UserVo)
def create_user(user:auth_schemas.User,db:Session= Depends(get_sqlite_db)):
    logger.info(f"user:{user.model_dump()}")
    logger.error(f"user:{user.model_dump()}")
    try:
        db_user = auth_service.get_user_by_name(user.username,db)
        if db_user:
            raise HTTPException(status_code=400,detail="User already exists")
        return auth_service.save_user(user,db)
    except Exception as e:
        logger.error(f"user:{user.model_dump()}",e)
        raise HTTPException(status_code=400,detail=str(e))


@auth_router.get("/get/{username}",response_model=auth_schemas.UserVo)
def get_user(username:str,db:Session= Depends(get_sqlite_db)):
    db_user = auth_service.get_user_by_name(username,db)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found")
    return db_user