import base_import as base_import
import config
from database import engine,Base
from auth.models import UserDB

Base.metadata.create_all(bind=engine)