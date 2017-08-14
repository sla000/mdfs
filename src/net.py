import socket

import struct

from log import *
import SocketServer
from utils import *

MAX_PKT_BUF_SIZE = 1024 * 1024 * 100

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

class TcpBaseHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        signature = self.request.recv(2)
        size = -1
        if signature == 'md':
            sizeStr = self.request.recv(4)
            size = struct.unpack("<I", sizeStr)[0]

        if signature != 'md' or size < 0 or size > MAX_PKT_BUF_SIZE:
            self.request.sendall(createPkt(8, 'Invalid'))
            self.server.close_request(self.request)

        buf = self.request.recv(int(size))
        self.handleConnection(self.request, size, buf)

    def handleConnection(self):
        raise Exception("Not implemented")