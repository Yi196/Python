import os
import logging
import traceback
from logging.handlers import RotatingFileHandler

def set_logger(logdir, basename, level=logging.DEBUG):
    # if not os.path.isdir(logdir):
    #     os.mkdir(logdir)
    os.makedirs(logdir, exist_ok=True)
    #    basename = os.path.basename(__file__)
    logname = os.path.join(logdir, 'log_' + basename + '.log')
    logger = logging.getLogger(__name__)
    logger.setLevel(level=level)

    if not logger.handlers:
        # 定义一个RotatingFileHandler，最多备份20个日志文件，每个日志文件最大50M
        rHandler = RotatingFileHandler(logname, maxBytes=50 * 1024 * 1024, backupCount=20)
        rHandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(filename)s - line: %(lineno)d - %(message)s')
        rHandler.setFormatter(formatter)

        # 设置日志在控制台输出
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        streamFormatter = logging.Formatter('%(levelname)s - %(asctime)s - %(filename)s - %(message)s')
        # 设置控制台中输出日志格式
        console.setFormatter(streamFormatter)

        logger.addHandler(console )
        logger.addHandler(rHandler)
    # logger.info('Start')
    return logger


if __name__ == '__main__':
    logdir = '../logs/'
    basename = os.path.splitext(os.path.basename(__file__))[0]
    logger = set_logger(logdir, basename)
    logger.info('123456')
    logger.warning('**Warning:123**')
    logger.error('**Error:123**')
    logger.critical('***********Program is not work！*************')