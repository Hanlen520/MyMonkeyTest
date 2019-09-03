# coding:utf-8

from Common.monkey_Config import Monkey_Config
from Common.adbComom import AdbCommon
from Common.monkeyCommon import MonkeyCommon
import time
from businessView.SendMail import send_mail
from Common.logger import Logger
from Common.fileCommon import Remove_file
import sys, os


def run():
    # 读取配置值
    devices = Monkey_Config()
    # 加载设配信息类
    adb = AdbCommon(devices.device)
    monkey = MonkeyCommon(devices)

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
                time.sleep(30)
        Logger('脚本停止执行')

        # 如果有错误日志，就发送邮件
        if monkey.writterError(devices.monkeylog, devices.writeerror) == 0:
            send_mail(devices.runtime * 60, adb, cmd, devices.monkeylog, devices.monkeyerrorlog, devices.writeerror)
        else :
            Logger('刪除空文件 : %s,%s'%(devices.writeerror,devices.monkeyerrorlog))
            Remove_file(devices.writeerror)
    else:
        Logger('安装失败')


if __name__ == '__main__':
    run()
    # 读取配置值
    # devices = Monkey_Config()
    # # 加载设配信息类
    # adb = AdbCommon(devices.device)
    # monkey = MonkeyCommon(devices)
    #
    # adb.installAPP(devices.apkname, devices.apkpath)
