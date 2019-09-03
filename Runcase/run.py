# coding:utf-8 

'''
命令行执行
@Author: LiuMei
在 Runcase的目录下执行 F:\python\MyMonkeyTest\Runcase> 不然会报错
python run.py --device 69d8ac6f  --seed 1001 --apkname com.nongfadai.android.beta3220 --throttle 500 --runtime 1 --loglevel INFO
'''

import sys, getopt
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import time
from Common.monkey_Config import Monkey_Config
from Common.adbComom import AdbCommon
from Common.monkeyCommon import MonkeyCommon
from businessView.SendMail import send_mail
from Common.logger import Logger
from Common.fileCommon import Remove_file


def run(argv):
    '''
    :return:
    '''
    device = ''
    seed = ''
    apkname = ''
    throttle = ''
    runtime = ''
    loglevel = ''

    # 读取配置值
    devices = Monkey_Config()
    # 加载设配信息类
    adb = AdbCommon(devices.device)
    monkey = MonkeyCommon(devices)

    example = 'python run.py --device 69d8ac6f  --seed 1001 --apkname com.nongfadai.android.beta3220 --throttle 500 --runtime 1 --loglevel INFO'

    try:
        options = ['device=', 'seed=', 'apkname=', 'throttle=', 'runtime=', 'loglevel=']
        opts, args = getopt.getopt(argv, 'd:s:a:t:r:l', options)

        for opt, arg in opts:
            if opt == '--device':
                devices.device = arg
            elif opt == '--seed':
                devices.seed = arg
            elif opt == '--apkname':
                devices.apkname = arg
            elif opt == '--throttle':
                devices.throttle = arg
            elif opt == '--runtime':
                devices.runtime = arg
            elif opt == '--loglevel':
                devices.loglevel = arg
            else:
                Logger('参考命令：%s' % example)


    except Exception as e:
        Logger(e)
        sys.exit()

    startTime = int(abs(round(time.time(), 0)))
    # 手机中是否有安装包
    if adb.installAPP(devices.apkname, devices.apkpath) == 0:
        # 存在就执行下一步

        # 清楚手机中的日志
        monkey.emptyLogcat()

        Logger('开始执行脚本')
        cmd = monkey.runMonkey()
        flag = True
        while flag:
            currentTime = int(abs(round(time.time(), 0)))
            Logger('已经运行时间：%d' % (currentTime - startTime))
            Logger('预期运行时间: %d' % (int(devices.runtime) * 60))
            if (currentTime - startTime) >= (int(devices.runtime) * 60):
                monkey.stopMonkey()
                flag = False
            else:
                Logger('等一会~，还没到时间呢')
                time.sleep(30)
        Logger('脚本停止执行')

        # 如果有错误日志，就发送邮件
        if monkey.writterError(devices.monkeylog, devices.writeerror) == 0:
            send_mail(devices.runtime * 60, adb, cmd, devices.monkeylog, devices.monkeyerrorlog, devices.writeerror)
        else:
            Logger('刪除空文件 : %s,%s' % (devices.writeerror, devices.monkeyerrorlog))
            Remove_file(devices.writeerror)
    else:
        Logger('安装失败')


if __name__ == '__main__':
    run(sys.argv[1:])
