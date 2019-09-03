# coding:utf-8 

'''
读取config配置
@Author: LiuMei
'''

from Common.fileCommon import readYaml
import time
import sys, os
from Common.logger import Logger

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Monkey_Config():

    def __init__(self):
        configYaml = readYaml('..\Config\MonkeyConfig.yaml')
        # 包名
        self.__apkname = configYaml['apkname']
        # 设备号
        self.__device = configYaml["device"]
        # 包的路径
        self.__apkpath = configYaml['apkpath']
        # 包是否是debug
        self.__appdebug = configYaml['appdebug']
        # 设备是否是模拟器
        self.__simulator = configYaml['simulator']

        # 设备运行时间
        self.__runtime = configYaml['runtime']
        # monkey 命令的send值
        self.__seed = configYaml['seed']
        # 时间间隔
        self.__throttle = configYaml['throttle']
        # 日志等级
        self.__loglevel = configYaml['loglevel']

        self.__monkeyfolder = 'MonkeyLog'
        self.__monkeylog = '../' + self.__monkeyfolder + '/%s_MonkeyInfo.log' % time.strftime('%Y-%m-%d-%H-%M')
        self.__monkeyerrorlog = '../' + self.__monkeyfolder + '/%s_MonkeyErrorLog.log' % time.strftime('%Y-%m-%d-%H-%M')
        self.__writeerror = '../' + self.__monkeyfolder + '/%s_WriteError.log' % time.strftime('%Y-%m-%d-%H-%M')

    @property
    def apkname(self):
        return self.__apkname

    @apkname.setter
    def apkname(self, value):
        Logger('要执行的包名是：  ' + value)
        self.__apkname = value

    @property
    def device(self):
        return self.__device

    @device.setter
    def device(self, value):
        Logger('设备号为：  ' + value)
        self.__device = value

    @property
    def apkpath(self):
        return self.__apkpath

    @apkpath.setter
    def apkpath(self, value):
        self.__apkpath = value

    @property
    def appdebug(self):
        return self.__appdebug

    @appdebug.setter
    def appdebug(self, value):
        self.__appdebug = value

    @property
    def simulator(self):
        return self.__simulator

    @simulator.setter
    def simulator(self, value):
        self.__simulator = value

    @property
    def runtime(self):
        try:
            if isinstance(int(self.__runtime), int):
                if int(self.__runtime) > 600:
                    Logger('最大运行时间是600分钟,大于600分钟会默认为600分钟')
                    return 600
                else:
                    return self.__runtime
        except Exception:
            Logger('输入的运行时间必须是整数，否则默认运行时间为10分钟')
            return 10

    @runtime.setter
    def runtime(self, value):
        try:
            if isinstance(int(value), int):
                if int(value) > 60:
                    Logger('最大运行时间是60分钟,大于60分钟会默认设置为60分钟')
                    self.__runtime = 60
                else:
                    Logger('执行时间设置为：  %s 分钟' % value)
                    self.__runtime = value
        except Exception:
            Logger('输入的运行时间必须是整数，否则默认运行时间为10分钟: ')
            self.__runtime = 10

    @property
    def seed(self):
        try:
            if isinstance(int(self.__seed), int):
                return self.__seed
            else:
                Logger('输入的send参数，类型必须是整数，否则send值默认为20')
                return 20
        except Exception:
            Logger('输入的send参数，类型必须是整数，否则send值默认为20')
            return 20

    @seed.setter
    def seed(self, value):
        try:
            if isinstance(int(value), int):
                Logger('seed值为：  ' + value)
                self.__seed = value
            else:
                Logger('输入的send参数，类型必须是整数，否则send值默认为20')
                self.__seed = 20
        except Exception:
            Logger('输入的send参数，类型必须是整数，否则send值默认为20')
            self.__seed = 20

    @property
    def throttle(self):
        try:
            if isinstance(int(self.__throttle), int):
                return self.__throttle
            else:
                Logger('输入的throttle参数，类型必须是整数，否则throttle值默认为500')
                return 500
        except Exception:
            Logger('输入的throttle参数，类型必须是整数，否则throttle值默认为500')
            return 500

    @throttle.setter
    def throttle(self, value):
        try:
            if isinstance(int(value), int):
                Logger('throttle的参数值为：  ' + value)
                self.__throttle = value
            else:
                Logger('输入的throttle参数，类型必须是整数，否则throttle值默认为500')
                self.__throttle = 500
        except Exception:
            Logger('输入的throttle参数，类型必须是整数，否则throttle值默认为500')
            self.__throttle = 500

    @property
    def loglevel(self):
        return self.__loglevel

    @loglevel.setter
    def loglevel(self, value):
        loglever = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
        if value in loglever:
            self.__loglevel = value
            Logger('日志级别设置为：  %s'% value)
        else:
            Logger('日志级别%s 不在%s中，日志级别设置为默认值：INFO' % (value, str(loglever)))
            self.__loglevel = 'INFO'

    @property
    def monkeyfolder(self):
        return self.__monkeyfolder

    @monkeyfolder.setter
    def monkeyfolder(self, value):
        self.__monkeyfolder = value

    @property
    def monkeylog(self):
        return self.__monkeylog

    @monkeylog.setter
    def monkeylog(self, value):
        self.__monkeylog = value

    @property
    def monkeyerrorlog(self):
        return self.__monkeyerrorlog

    @monkeyerrorlog.setter
    def monkeyerrorlog(self, value):
        self.__monkeyerrorlog = value

    @property
    def writeerror(self):
        return self.__writeerror

    @writeerror.setter
    def writeerror(self, value):
        self.writeerror = value


if __name__ == '__main__':
    c = Monkey_Config()
    Logger(c.runtime)
    Logger(c.device)
    c.runtime = 70
    Logger(c.runtime)

    c.runtime = 'oo'
    Logger(c.runtime)
