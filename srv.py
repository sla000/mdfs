#!/usr/bin/python

from conserv import *
from topserver import *

s = ConnectionServer()
s.daemonize()

topManager = TopServerManager(2)
topManager.run()

time.sleep(100)
