# coding:utf-8 

'''
执行和关闭monkey
@Author: LiuMei
'''

import os
from Common.monkey_Config import Monkey_Config
import subprocess
from time import sleep
import re
from Common.logger import Logger


class MonkeyCommon():
    def __init__(self, devices):

        self.devices = devices
        # 发生事件总数，100W
        self.event = pow(10, 5)

    def runMonkey(self):
        '''
        执行Monkey
        :return:
        '''
        # 检查上一级目录是否存在某文件夹？
        # if not os.path.exists(self.devices.monkeyfolder):
        #     os.mkdir(self.devices.monkeyfolder)

        # adb -s %s shell monkey 指定设备运行monkey
        # -s
        # -p 指定包名
        # --hprof 指定该项后在事件序列发送前后会立即生成分析报告
        # --throttle
        # --ignore-crashes 忽略奔溃
        # --ignore-timeouts 忽略超时
        # --ignore-security-exceptions 忽略安全异常
        # --monitor-native-crashes 用于指定是否监视并报告应用程序发生崩溃的本地代码
        # --pct-syskeys 系统事件的百分比
        cmd = 'adb -s %s shell monkey ' \
              '-s %d ' \
              '-p %s ' \
              '--hprof ' \
              '--throttle %d ' \
              '--ignore-crashes ' \
              '--ignore-timeouts ' \
              '--ignore-security-exceptions ' \
              '--ignore-native-crashes ' \
              '--monitor-native-crashes ' \
              '--pct-syskeys 10 ' \
              '-v -v -v %d 1>%s 2>%s' % \
              (self.devices.device, int(self.devices.seed), self.devices.apkname, int(self.devices.throttle),
               self.event, self.devices.monkeylog, self.devices.monkeyerrorlog)
        Logger(cmd)
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        return cmd

    def stopMonkey(self):
        '''
        停止monkey
        :return:
        '''
        sleep(1)
        try:
            grep_cmd = 'adb -s %s shell ps | findstr monkey' % self.devices.device
            Logger(grep_cmd)
            pipe = os.popen(grep_cmd)
            result = pipe.read()
            Logger(result)
            if result == '':
                Logger('monkey进程不存在 : %s'%grep_cmd)
            else:
                Logger('monkey 进程存在 : %s'%grep_cmd)
                pid = result.split()[1]
                stop_cmd = 'adb -s %s shell kill %s' % (self.devices.device, pid)
                Logger(stop_cmd)
                os.system(stop_cmd)
        except Exception:
            Logger('停止 monkey 异常')

    def emptyLogcat(self):
        '''
        monkey运行前执行 adb logcat -c 清空所有log缓存日志
        :return:
        '''
        try:
            Logger('使用adb logcat -c 清空手机中的log')
            os.popen('adb -s %s logcat -c' % self.devices)
            return 0
        except Exception as e:
            Logger('执行adb logcat -c 出现异常： %s' % e)
            return 1

    def writterError(self, monkeyInfoPath, wirteErrorPath):
        '''
        解析log文件中是否有crash，ANR等错误，有的话写入writerErrorPath文件中
        :param monkeyInfoPath:  monkey日志文件地址
        :param wirteErrorPath: 错误日志写入的文件地址
        :return: 0 表示有错误日志 1表示没有错误日志
        '''
        # monkeyInfoPath = self.devices.monkeylog
        # wirteErrorPath = self.devices.writeerror
        try:
            f = open(monkeyInfoPath, 'r')
            lines = f.readlines()
            if len(lines) == 0:
                Logger('%s 路径的日志为空' % monkeyInfoPath)
            else:
                fr = open(wirteErrorPath, 'a', encoding='utf-8')
                for line in lines:
                    if (re.findall('CRASH', line) or
                            re.findall('ANR', line) or
                            re.findall('No Response', line)):
                        # 找到行数
                        number = lines.index(line) + 1
                        fr.write('第%s行' % number + ',' + '错误原因: %s' % line)
                        fr.write('\n')
                f.close()
                fr.close()
                if os.path.getsize(wirteErrorPath) == 0:
                    Logger('扫描%s路径下的日志未发现错误日志' % monkeyInfoPath)
                    # os.system('rm -rf %s' % wirteErrorPath)
                    return 1
                else:
                    Logger('扫描%s路径下的日志发现错误日志,过滤后的文件路径%s' % (monkeyInfoPath, wirteErrorPath))
                    return 0
        except Exception as e:
            Logger('解析日志文件报错: %s' % e)
            return 1


if __name__ == '__main__':
    b = Monkey_Config()
    c = MonkeyCommon(b)
    # cmd = c.runMonkey()
    # sleep(60)
    # c.stopMonkey()
    # Logger(b.writeerror)
    c.writterError('../MonkeyLog/MonkeyInfo_20190821094934.log', '../MonkeyLog/MonkeyErrorLog_20190821094934.log')
    # Logger(os.path.getsize('../MonkeyLog/WriteError_20190820205740.log'))
