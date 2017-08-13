#!/usr/bin/python
import random

from ssh import *
from lxc import * 

USER = 'ubuntu'
PASSWD = 'ubuntu'
PATH = '/home/ubuntu/src1'

class Deployer:
    def __init__(self, ip):
        self.ip = ip
        self.user = USER
        self.passwd = PASSWD
        self.ssh = Ssh(self.ip, self.user, self.passwd)
        self.ssh.connect()

    def pushSrc(self):
        self.ssh.push('../../src', PATH)
    def cleanContainers(self):
        self.ssh.execute('rm -rf ' + PATH)
    def addConnServIPToConfig(self, ip):
        print self.ssh.execute('sed -i "s/CONN_SERV_IP.*=.*/CONN_SERV_IP = \'%s\'/g" %s'  % (ip, os.path.join(PATH, 'config.py')))

if __name__ == '__main__':
    ips = Lxc.getContainersIP()

    connServNum = 1
    connServList = ips[:connServNum]
    tops = ips[connServNum:]

    for ip in connServList:
        dep = Deployer(ip)
        dep.pushSrc()
        dep.ssh.execute('rm -rf /tmp/*.log')
        dep.ssh.execute('cd %s && python %s' % (PATH, 'conserv.py'))

    for ip in tops:
        dep = Deployer(ip)
        dep.pushSrc()
        randConnServIP = connServList[random.randint(0, connServNum-1)]
        dep.addConnServIPToConfig(randConnServIP)

        dep.ssh.execute('rm -rf /tmp/*.log')
        dep.ssh.execute('python %s' % os.path.join(PATH, 'topserver.py'))

    os.unlink('src.tar.gz')
    os.system('rm -rf /tmp/*.log')
