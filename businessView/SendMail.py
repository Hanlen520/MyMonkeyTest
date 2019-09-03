# coding:utf-8 

'''
发送邮件类
@Author: LiuMei
'''

from Common.mail_Config import Mail_Config
from Common.adbComom import AdbCommon
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import time


def send_mail(Runtime, adb, cmd, monkeylog, monkeyerrorlog, writeerror):
    '''
    邮件发送
    :param Runtime: monkey开始执行时间
    :param adb:  AdbCommon实例
    :param cmd:  monkey脚本
    :param monkeylog:  monkey日志地址
    :param monkeyerrorlog:  错误日志地址
    :param writeerror:  错误日志写入文件
    :return:
    '''
    mail = Mail_Config()
    # 收件人和发件人
    receiver = mail.debuglist
    sender = mail.mail_user
    # 发件人邮箱的SMTP服务器
    smtpserver = mail.mail_host
    smtpport = mail.mail_port
    # 发件人邮箱的用户名和授权码
    username = mail.mail_user
    password = mail.mail_password

    mail_title = 'monkey测试预警'

    # 邮件正文
    info = adb.getProductInfo()
    mail_content = setMail_content(Runtime, info[0], info[1], info[2], cmd, writeerror)

    # 创建一个带附件的实例
    message = MIMEMultipart()
    Logger(dir(message))
    message['From'] = '布谷农场APP测试<%s>' % sender
    message['To'] = ';'.join(receiver)
    message['Subject'] = Header(mail_title, 'utf-8')
    Logger('创建实例成功')
    # 添加正文
    message.attach(MIMEText(mail_content, 'plain', 'utf-8'))

    # 构造附件
    att1 = MIMEText(open(monkeylog).read())
    att1['Content-Type'] = 'application/octet-stream'
    att1['Content-Disposition'] = 'attachment;filename="info.log"'
    message.attach(att1)

    att2 = MIMEText(open(monkeyerrorlog).read())
    att2['Content-Type'] = 'application/octet-stream'
    att2['Content-Disposition'] = 'attachment;filename="error.log"'
    message.attach(att2)

    try:
        smtp = smtplib.SMTP_SSL(smtpserver, smtpport)
        smtp.connect(smtpserver)
        smtp.set_debuglevel(1)
        smtp.login(username, password)

        # 发送邮件   发件人#收件人#邮件内容
        smtp.sendmail(sender, receiver, message.as_string())

        smtp.quit()
        Logger('发送邮件成功')
    except Exception:
        Logger('发送邮件失败')


def setMail_content(Runtime, brand, model, version, cmd, writeerror):
    '''
    拼接邮件中的content内容
    :param Runtime: 运行开始时间
    :param brand:  设备品牌
    :param model: 设备型号
    :param version: 设备系统号
    :param cmd:  cmd命令
    :param writeerror:  错误日志内容文件地址
    :return: 
    '''
    try:
        with open(writeerror, 'r',encoding='utf-8') as f:
            error = f.read()

        sendtime = time.strftime("%Y-%m-%d %H:%M:%S")

        content = '''
        发生时间: %s 
    
        测试时长: %s秒
    
        设备品牌:%s
    
        设备型号:%s
    
        设备系统:%s
    
        monkey执行命令：%s
    
        错误日志标记: %s
    
        monkey日志详见附件''' % \
                  (sendtime, Runtime, brand, model, version, cmd, error)
        return content
    except Exception as e:
        Logger(e)
        return 'monkey遇到异常'


if __name__ == '__main__':
    # adb = AdbCommon('MYV0215726012219')
    # send_mail('2019-08-07', adb, 'monkey脚本',  '../MonkeyLog/MonkeyInfo_20190821094934.log',
    #           '../MonkeyLog/MonkeyErrorLog_20190821094934.log', '../MonkeyLog/WriteError_20190821094934.log')
    content = setMail_content('2019-08-07', 'ddd', 'vv', 'ffff', 'monkey脚本',
                              '../MonkeyLog/20190828102557_WriteError.log')

    Logger(content)
