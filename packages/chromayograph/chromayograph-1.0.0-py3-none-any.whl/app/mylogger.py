import logging
import os

# 单例模式的logger
_logger = None

def get_logger(name='mylogger', log_file=None):
    global _logger
    if _logger is None:
        # 创建一个logger
        _logger = logging.getLogger(name)
        _logger.setLevel(logging.DEBUG)  # 设置默认日志级别

        # 创建一个控制台处理器，并设置日志级别为DEBUG
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 创建一个格式化器，并将其添加到处理器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # 将处理器添加到logger
        _logger.addHandler(ch)

        if log_file:
            # 创建一个文件处理器，并设置日志级别为DEBUG
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            _logger.addHandler(fh)

    return _logger
