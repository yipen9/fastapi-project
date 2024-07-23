# module specific business logic
from sqlalchemy.orm import Session
from auth.models import UserDB
from auth.schemas import User
import auth.dependencies as auth_dependencies
import auth.crud as auth_crud 


def save_user(user:User,db:Session):
    userDB =  auth_crud.create_user(db,user,auth_dependencies.get_password_hash(user.password))
    return userDB
    

def get_user_by_name(username:str,db:Session):
    return auth_crud.get_user_by_username(db,username)