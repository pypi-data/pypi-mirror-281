import os
from appdirs import user_data_dir

def get_file_path(name):
    data_dir = user_data_dir(appname='qhelper', appauthor=False)
    # 创建数据目录（如果不存在）
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, name)