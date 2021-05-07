"""
读取配置文件工具类

@author sven
@create 2021-05-06
"""
import os
import json
import traceback
from utils.log_util import get_logger

get_log = get_logger('config_util.log', level="INFO")

current_path = os.path.abspath(__file__)
config_basic_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."), 'config')


def read_mns_config():
    try:
        config_file = open(os.path.join(config_basic_path, 'mns.conf'), 'r')
        config = config_file.read()
        config_file.close()
        config = json.loads(config)
        return config['access_id'], config['access_key'], config['endpoint'], config['token']
    except Exception as e:
        get_log.info(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
        return None

