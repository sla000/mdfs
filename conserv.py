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
        f = open('aa.log' , 'a+')
        f.write(str(buf))
        f.close()

class ReuseTcpServer(SocketServer.TCPServer):
    allow_reuse_address = True

class ConnectionServer(Daemon):
    def __init__(self):
        self.addr = (getSelfIP(), CONN_SERV_PORT)
        Daemon.__init__(self)
        SocketServer.TCPServer.allow_reuse_address = True
        self.server = SocketServer.TCPServer(self.addr, ConnectionServerHandler)

    def main(self):
        self.server.serve_forever()
    def onexit(self):
        self.server.server_close()


class TopServerHandler(TcpBaseHandler):
    def handleConnection(self, sock, size, buf):
        print 'size = ' + str(size)
        print "buf: " + str(buf)


class TopServer(Daemon):
    def __init__(self, ipConnServ, ip, port):
        self.addr = (ip, port)
        Daemon.__init__(self)
        self.connServClient = ConnectionServerClient(ipConnServ, ip, port)

    def main(self):
        self.connServClient.daemonize()
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer(self.addr, TopServerHandler)
        server.serve_forever()

class ConnectionServerClient(Daemon):
    def __init__(self, ipConnServ, ip, port):
        self.addr = (ipConnServ, CONN_SERV_PORT)
        self.ip = ip
        self.port = port
    def getConnServIP(self):
        # TODO: fix it
        return getSelfIP()
    def main(self):
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.addr)

            pkt = 'On' + '*'
            pkt += self.ip + ':'
            pkt += str(self.port)

            sock.sendall(createPkt(len(pkt), pkt))
            time.sleep(OFFLINE_TIME)



