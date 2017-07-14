#!/usr/bin/python

from requests import *


nlist = [ Neighbour('10.10.10.10', 8001, uuid.uuid4().hex ), Neighbour('10.10.10.11', 8002, uuid.uuid4().hex ) ]

s = GetNeighboursReqA().create( nlist) 


nlist = GetNeighboursReqA().parse(s)
assert GetNeighboursReqA().create(nlist) == s, "Failed neighbour test"
print GetNeighboursReqA().pkt(nlist)

print "Test ok" 
