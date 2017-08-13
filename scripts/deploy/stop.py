#!/usr/bin/python
from run import *

ips = Lxc.getContainersIP()



for num, ip in enumerate(ips):
    print ip
    dep = Deployer(ip)
    dep.ssh.execute('cd %s && python %s' % (PATH, 'halt.py'))
    try:
        dep.ssh.pull('/tmp/connserv.log', '/tmp/cs%i.log' % num)
    except:
        pass

    try:
        dep.ssh.pull('/tmp/topserver.log', '/tmp/top%i.log' % num)
    except:
        pass

