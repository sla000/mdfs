import socket
import struct
import sys

import time

from utils import *

OFFLINE_TIME = 5

CONN_SERV_PORT=4545

MAX_PKT_BUF_SIZE = 1024 * 1024 * 100



import SocketServer

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


class ConnectionServerHandler(TcpBaseHandler):
    def handleConnection(self, sock, size, buf):
        print 'size = ' + str(size)
        print "buf: " + str(buf)


class ConnectionServer(Daemon):
    def __init__(self):
        self.addr = (getSelfIP(), CONN_SERV_PORT)

    def main(self):
        server = SocketServer.TCPServer(self.addr, ConnectionServerHandler)
        server.serve_forever()


class ConnectionServerClient(Daemon):
    def __init__(self):
        self.addr = (self.getConnServIP(), CONN_SERV_PORT)
    def getConnServIP(self):
        # TODO: fix it
        return getSelfIP()
    def main(self):
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.addr)
            sock.sendall(createPkt(6, "alive"))
            time.sleep(OFFLINE_TIME)



