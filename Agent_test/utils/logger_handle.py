'''
提供日志信息
'''

import logging
from path_tools import get_abs_path
import os
from datetime import datetime

# 日志目录
LOG_ROOT = get_abs_path(r"logs")

os.makedirs(LOG_ROOT, exist_ok=True)

DEFAULT_LOG_FORMAT  = logging.Formatter(
    # 时间-名称-级别-文件名-行号-信息
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)



def get_logger(
        name: str = 'agent',
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,    #DEBUG 更详细
        log_file: str = None)-> logging.Logger:
    '''
    获取日志对象
    '''
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置全局日志级别

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    # 文件处理器
    if log_file is None:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = get_logger()  # 默认日志对象

if __name__ == "__main__":
    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.error("This is an error message.")   