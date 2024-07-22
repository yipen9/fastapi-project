import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

