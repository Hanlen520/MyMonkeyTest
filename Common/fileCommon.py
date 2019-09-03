# coding:utf-8 

'''
文件操作类
@Author: LiuMei
'''

import yaml
import os
from Common.logger import Logger


def readYaml(file_path):
    '''
    读取yaml文件
    :return:
    '''
    with open(file_path, 'r', encoding='utf-8') as c:
        content = yaml.load(c.read())
    return content


def Remove_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            Logger('成功刪除文件 ：%s' % file_path)
        else:
            Logger('不存在文件夾：%s' % file_path)
    except Exception as e:
        Logger('刪除文件拋出異常：%s' % e)
