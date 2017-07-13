#!/usr/bin/python

from requests import *

s = GetNeighboursReqA().create( [ ('10.10.10.10', 8001, uuid.uuid4().hex ), ('10.10.10.11', 8002, uuid.uuid4().hex ) ] ) 
nlist = GetNeighboursReqA().parse(s)
nlist = map(lambda x: (x.ip, x.port, x.gid), nlist)

assert GetNeighboursReqA().create(nlist) == s, "Failed neighbour test"
print GetNeighboursReqA().pkt(nlist)

print "Test ok" 
