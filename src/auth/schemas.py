 # pydantic models
from enum import Enum
from pydantic import AnyUrl, BaseModel, EmailStr, Field,field_validator
from typing import Union
from schemas import CustomModel
from datetime import datetime
# token的格式
class Token(CustomModel):
    access_token: str
    token_type: str

# token中access_token存储的（k,v）对中，key = "sub"关键字对应的值。可以采有usr_id等，更便于查询。
class TokenData(CustomModel):
    username: Union[str,None] = None


class MusicBand(str, Enum):
   AEROSMITH = "AEROSMITH"
   QUEEN = "QUEEN"
   ACDC = "AC/DC"


1
class User(CustomModel):
    username: str = Field(min_length=1, max_length=128, pattern="^[A-Za-z0-9-_]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    age: int = Field(ge=18, default=None)  # must be greater or equal to 18
    favorite_band: MusicBand | None = None  # only "AEROSMITH", "QUEEN", "AC/DC" values are allowed to be inputted
    website: AnyUrl | None = None
    created: datetime = Field(default_factory=datetime.now)

    @field_validator("password")
    def is_password_secure(cls, v):
        if not any(c.islower() for c in v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not any(not c.isalnum() for c in v):
            raise ValueError('密码必须包含至少一个特殊字符')
        return v
    

class UserVo(CustomModel):
    username: str
    email: EmailStr
    favorite_band: MusicBand | None
    website: AnyUrl | None
    created: datetime

    class Config:
        orm_mode = True