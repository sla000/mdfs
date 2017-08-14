import socket
import struct
import sys

import time

from utils import *
import uuid

from neighbour import *

class Pkt:
    SIG = 'unknown'
    @classmethod
    def parse(cls, pktBuf):
        sig = pktBuf.split('*')[0]
        assert sig == cls.SIG, '%s == %s' % (sig, self.SIG)
        return cls.parseInternal(''.join(pktBuf.split('*')[1:]))
    @classmethod
    def create(cls, *args):
        s = cls.SIG + '*'
        s += cls.createInternal(*args)
        return s
    @classmethod
    def pkt(cls, *args):
        pktStr = cls.create(*args)
        return createPkt(len(pktStr), pktStr)
    @classmethod
    def parseInternal(cls, pkt):
        pass
    @classmethod
    def createInternal(cls, *args):
        pass

class GetNeighboursReq(Pkt):
    SIG ='GetNeighboursReq' 

    @classmethod
    def parseInternal(cls, pkt):
        return pkt
    @classmethod
    def createInternal(cls, topId):
        return topId

class GetNeighboursReqA(Pkt):
    SIG ='GetNeighboursReqA'
    @classmethod
    def parseInternal(cls, pkt):
        nghList = pkt.split('#')
        return map(lambda x: Neighbour.fromStr(x), nghList)
    # neighbourList = [ (ip, port, gid) ]
    @classmethod
    def createInternal(cls, neighbourList):
        nstrList = map(lambda neghbour :  str(neghbour), neighbourList)
        return '#'.join(nstrList)
        
class TopServerOnlineReq(Pkt):
    SIG='TopServerOnlineReq'
    @classmethod
    def parseInternal(cls, pkt):
        tmp = pkt.split(':')
        assert len(tmp) == 3
        ip = tmp[0]
        port = int(tmp[1])
        ID = tmp[2]
        return ip, port, ID
    @classmethod
    def createInternal(cls, ip, port, ID):
        return '%s:%u:%s' % (ip, port, ID)

class ExitReq(Pkt):
    SIG='Exit'
    @classmethod
    def parseInternal(cls, pkt):
        return pkt
    @classmethod
    def createInternal(cls):
        return ''

class GetFileIDReq(Pkt):
    SIG='GetFileIDRequest'
    @classmethod
    def parseInternal(cls, pkt):
        return pkt
    @classmethod
    def createInternal(cls, fileHash):
        return fileHash

class GetFileIDResp(Pkt):
    SIG='GetFileIDResponse'
    @classmethod
    def parseInternal(cls, pkt):
        return pkt
    @classmethod
    def createInternal(cls, fileID):
        return fileID

