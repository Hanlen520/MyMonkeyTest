# coding:utf-8 

'''

@Author: LiuMei
'''
import os


def devices():
    '''
    获取设备号
    :return:
    '''
    try:
        cmd = 'adb devices'
        result = os.popen(cmd)
        m = result.read()
        device = m.replace('List of devices attached\n', '').replace('device', '')
        print(m+'\n--------------------------------')
        return device
    except Exception as e:
        print('设备号获取失败 : %s' % e)


device = devices()

m = os.popen('adb -s %s shell getprop ro.product.model' % device)
b = os.popen('adb -s %s shell getprop ro.product.brand' % device)
v = os.popen('adb -s %s shell getprop ro.build.version.release' % device)
model = m.read().replace('\n', '').replace('\r', '')
brand = b.read().replace('\n', '').replace('\r', '')
version = v.read().replace('\n', '').replace('\r', '')

print(model+'&&&'+brand+'&&&'+version)
