#!/usr/bin/python

from conserv import *

s = ConnectionServer()
s.daemonize()

c1 = TopServer(getSelfIP(), getSelfIP(), 8000)
c1.main()

