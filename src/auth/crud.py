from sqlalchemy.orm import Session
from auth.models import UserDB
from auth.schemas import User


def get_user(db:Session,user_id:int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()

def get_user_by_email(db:Session,email:str):
    return db.query(UserDB).filter(UserDB.email == email).first()

def get_user_by_username(db:Session,username:str):
    return db.query(UserDB).filter(UserDB.username == username).first()


def create_user(db:Session,user:User,hashPassword:str):
    db_user = UserDB(username=user.username,age=user.age,hashed_password=hashPassword,email=user.email,
                     favorite_band=user.favorite_band,website=str(user.website),created=user.created)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
