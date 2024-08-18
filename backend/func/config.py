import json
import socket

from GameCloud.settings import BASE_DIR

HOSTNAME = socket.gethostname()
CURRENT_IP = socket.gethostbyname(HOSTNAME)


# 检查config.json文件是否存在
def check_config():
    """
    检查文件是否存在
    :return:
    """
    if not (BASE_DIR / 'config.json').exists():
        with open(BASE_DIR / 'config.json', 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)


def get_config(key):
    """
    获取配置文件信息
    :param key:
    :return:
    """
    check_config()
    with open(BASE_DIR / 'config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        return config.get(key)


def set_config(key, value):
    """
    设置配置文件信息
    :param key:
    :param value:
    :return:
    """
    try:
        with open(BASE_DIR / 'config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            config[key] = value
            with open(BASE_DIR / 'config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        check_config()
        with open(BASE_DIR / 'config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            config[key] = value
            with open(BASE_DIR / 'config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)


check_config()
