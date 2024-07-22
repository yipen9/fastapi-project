 # global configs
import os
from dotenv import load_dotenv


def __load_env():
    load_dotenv()

__load_env()


def get_conf(key, default=None):
    return os.getenv(key, default)


DATABASE_URL = get_conf('DATABASE_URL')