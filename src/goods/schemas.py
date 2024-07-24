 # pydantic models
from enum import Enum
from pydantic import AnyUrl, BaseModel, EmailStr, Field,field_validator
from typing import Union
from schemas import CustomModel
from datetime import datetime

class Goods(CustomModel):
    goood_code: str = Field(min_length=1, max_length=32)
    good_name: str = Field(min_length=1, max_length=128)
    price: float = Field(ge=0)
    
    
class GoodVo(CustomModel):
    id: int
    good_code: str
    good_name: str
    price: float
    created: datetime

    class Config:
        orm_mode = True