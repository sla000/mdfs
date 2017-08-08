#!/usr/bin/python

from conserv import *
from topserver import *

s = ConnectionServer()
s.daemonize()

topManager = TopServerManager(100)
topManager.run()

time.sleep(1)
topList[0].connServClient.getNeighbours()
time.sleep(100)
