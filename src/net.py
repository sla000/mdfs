import socket

import struct

from log import *



def getConnectedSock(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
    except:
        log.d('Connect failed to: %s %u' % (ip, port))
    return sock

def recvPkt(sock):
    try:

        md = sock.recv(2)
        assert len(md) == 2
        szStr = sock.recv(4)
        assert len(szStr) == 4
        sz = struct.unpack('<I', szStr)[0]
        buf = sock.recv(sz)
        assert len(buf) == sz
        return buf
    except Exception as e:
        log.e('Failed to recv pkt. ' + e.__class__ + ' ' + e.message)
        return ''

def sendPkt(sock, pkt):
    sock.sendall(pkt)
