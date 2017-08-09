import socket
import struct
import sys

import time

from utils import *
import uuid

from neighbour import *

class Pkt:
    def __init__(self):
        self.SIG = 'unknown'
    def parse(self, pktBuf):
        sig = pktBuf.split('*')[0]
        assert sig == self.SIG, '%s == %s' % (sig, self.SIG)
        return self.parseInternal(''.join(pktBuf.split('*')[1:]))
    def create(self, *args):
        s = self.SIG + '*'
        s += self.createInternal(*args)
        return s
    def pkt(self, *args):
        pktStr = self.create(*args)
        return createPkt(len(pktStr), pktStr)
    def parseInternal(self, pkt):
        pass
    def createInternal(self, *args):
        pass

class GetNeighboursReq(Pkt):
    SIG ='GetNeighboursReq' 
    def __init__(self):
        self.SIG = GetNeighboursReq.SIG 
    def parseInternal(self, pkt):
        return pkt
    def createInternal(self, topId):
        return topId

class GetNeighboursReqA(Pkt):
    SIG ='GetNeighboursReqA' 
    def __init__(self):
        self.SIG = GetNeighboursReqA.SIG 
    def parseInternal(self, pkt):
        nghList = pkt.split('#')
        return map(lambda x: Neighbour.fromStr(x), nghList)
    # neighbourList = [ (ip, port, gid) ]
    def createInternal(self, neighbourList):
        nstrList = map(lambda neghbour :  str(neghbour), neighbourList)
        return '#'.join(nstrList)
        
class TopServerOnlineReq(Pkt):
    SIG='TopServerOnlineReq'
    def __init__(self):
        self.SIG = TopServerOnlineReq.SIG
    def parseInternal(self, pkt):
        tmp = pkt.split(':')
        assert len(tmp) == 3
        ip = tmp[0]
        port = int(tmp[1])
        ID = tmp[2]
        return ip, port, ID
    def createInternal(self, ip, port, ID):
        return '%s:%u:%s' % (ip, port, ID)

class ExitReq(Pkt):
    SIG='Exit'
    def __init__(self):
        self.SIG =  ExitReq.SIG
    def parseInternal(self, pkt):
        return pkt
    def createInternal(self):
        return ''


        

