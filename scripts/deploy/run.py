#!/usr/bin/python
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

print 'dsfsd'
ips = Lxc.getContainersIP()
print ips
dep = Deployer(ips[0])
dep.pushSrc()

