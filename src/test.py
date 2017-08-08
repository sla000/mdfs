#!/usr/bin/python

from utils import *
import time

class DaemonTest(Daemon):
    def __init__(self):
        Daemon.__init__(self)
    def main(self):
        print "aaaa"
        time.sleep(100)


dt = DaemonTest()
dt.daemonize()
dt.kill()
print dt.pid

time.sleep(100)
