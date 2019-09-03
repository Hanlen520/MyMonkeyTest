# coding:utf-8 

'''
读取邮箱配置
@Author: LiuMei
'''
from Common.fileCommon import readYaml


class Mail_Config():
    def __init__(self):
        configYaml = readYaml('..\Config\MailConfig.yaml')
        self.__mail_host = configYaml['mail_host']
        self.__mail_port = configYaml['mail_port']
        self.__mail_user = configYaml['mail_user']
        self.__mail_password = configYaml['mail_password']
        self.__mail_postfix = configYaml['mail_postfix']
        self.__debuglist = configYaml['debuglist']
        self.__receiverlist = configYaml['receiverlist']

    @property
    def mail_host(self):
        return self.__mail_host

    @property
    def mail_port(self):
        return self.__mail_port

    @property
    def mail_user(self):
        return self.__mail_user

    @property
    def debuglist(self):
        return self.__debuglist

    @property
    def mail_postfix(self):
        return self.__mail_postfix

    @property
    def mail_password(self):
        return self.__mail_password

    @property
    def receiverlist(self):
        return self.__receiverlist


if __name__ == '__main__':
    m = Mail_Config()
    Logger(m.receiverlist[1])
    Logger(type(m.debuglist))
    Logger(m.mail_host)
