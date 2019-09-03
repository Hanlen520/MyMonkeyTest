# coding:utf-8 

'''
日志打印
@Author: LiuMei
'''

import logging
import time


def Logger(message):
    project_name = 'monkeytest'
    log_file_name = project_name + '_' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'

    log_file_folder = '../Log/'
    log_file_str = log_file_folder + log_file_name

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # %(filename)s[line:%(lineno)d]
    logger_format = logging.Formatter(fmt='%(levelname)s:%(asctime)s  %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
    # 文件输出
    logger_file = logging.FileHandler(log_file_str, encoding='utf-8')
    logger_file.setFormatter(logger_format)
    logger.addHandler(logger_file)
    logger.info(message)
    logger.removeHandler(logger_file)

    # 控制台输出
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logger_format)
    logger.addHandler(console)
    logger.info(message)
    logger.removeHandler(console)


if __name__ == '__main__':
    Logger('this is debug log')
