"""
日志工具类

@author sven
@create_date 2018-07-04
"""

import logging
import os

current_path = os.path.abspath(__file__)


def get_logger(name, level='INFO'):
    """
    返回一个logger对象，
    默认log总开关为INFO
    控制台handle的log等级为DEBUG,文件handle的log等级为WARNING
    """
    log_basic_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."), 'log', '{}')
    if not os.path.exists(log_basic_path.replace("{}", "")):
        os.makedirs(log_basic_path.replace("{}", ""), exist_ok=True)

    logger = logging.getLogger(name)
    logger.propagate = False

    if level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif level == 'INFO':
        logger.setLevel(logging.INFO)
    elif level == 'WARNING':
        logger.setLevel(logging.WARNING)
    elif level == 'ERROR':
        logger.setLevel(logging.ERROR)
    elif level == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

    # 创建一个handler，用于写入日志文件
    logfile = log_basic_path.format(name)
    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.INFO)   # 输出到file的log等级的开关
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()  # 输出到pycharm控制台
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    # 将logger添加到handler里面
    if logger.hasHandlers():  # 防止重复输出日志
        logger.handlers.clear()
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
