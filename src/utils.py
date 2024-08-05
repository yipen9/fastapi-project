import os
from datetime import datetime
def get_project_path():
    script_path = os.path.abspath(__file__)
    path = os.path.join(script_path,"..","..")
    return os.path.abspath(path)


def get_abs_path(*relative_path):
    return os.path.join(get_project_path(), *relative_path)


def get_now_time():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    print(get_project_path())
    print(get_abs_path("resources","word_dict.json"))


