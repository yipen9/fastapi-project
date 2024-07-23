 # global configs
import os
from dotenv import dotenv_values


def __load_env():
    config = dotenv_values("src/.env")
    return config

__config = __load_env()

def get_conf(key, default=None):
    return __config.get(key, default)


def get_number(s):
    try:
        num = int(s)
        return num
    except ValueError:
        pass
    return s

SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,            # 连接池大小
        'max_overflow': 10,        # 允许超出连接池大小的连接数
        'pool_timeout': 30,        # 获取连接的超时时间（秒）
        'pool_recycle': 1800,      # 连接被回收前的存活时间（秒）
        'connect_args': {'check_same_thread': False}  # SQLite 特有参数
    }