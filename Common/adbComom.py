# coding:utf-8 

'''
获取设备信息
@Author: LiuMei
'''

import os
from Common.logger import Logger


class AdbCommon():

    def __init__(self, device):
        self.device = device


    def inspectapp(self, apkname):
        '''
        检测APP是否存在
        :param apkname:
        :return:
        '''
        try:
            cmd = 'adb -s %s shell pm list packages' % self.device
            result = os.popen(cmd)
            if apkname in result.read():
                Logger('%s 存在' % apkname)
                return 0
            else:
                Logger('%s 不存在' % apkname)
                return 1
        except Exception:
            Logger('%s 检测失败' % apkname)
            return 1

    def getProductInfo(self):
        '''
        获取当前设备的信息
        :return: 设备信息
        '''
        try:

            m = 'unidefined'
            # 品牌
            b = 'unidefined'
            # 系统版本号
            v = 'unidefined'
            # 手机型号
            m = os.popen('adb -s %s shell getprop ro.product.model' % self.device)
            b = os.popen('adb -s %s shell getprop ro.product.brand' % self.device)
            v = os.popen('adb -s %s shell getprop ro.build.version.release' % self.device)

            model = m.read().replace('\n', '').replace('\r', '')
            brand = b.read().replace('\n', '').replace('\r', '')
            version = v.read().replace('\n', '').replace('\r', '')
            return brand, model, version
        except Exception:
            Logger("获取手机型号报错")
            return 'unidefined' 'unidefined' 'unidefined'

    def installAPP(self, apkname, apkpath):
        '''
        安装安装包
        :param apkname: 安装包名称
        :param apkpath: 安装包路径
        :return: 0 安装成功 1安装失败
        '''
        try:
            if self.inspectapp(apkname) == 0:
                Logger('已有安装包')
                return 0
            else:
                cmd = 'adb -s %s install %s' % (self.device, apkpath)
                os.system(cmd)
                if self.installAPP(apkname) == 0:
                    Logger('安装安装包成功')
                    return 0
                else:
                    Logger('安装安装包失败')
                    return 1
        except Exception as e:
            Logger('安装安装包失败/n' + e)
            return 1


if __name__ == '__main__':
    a = AdbCommon('MYV0215726012219')
    # Logger(a.inspectapp('com.nongfadai.android'))
    # Logger(a.getProductInfo())
    a.installAPP()
