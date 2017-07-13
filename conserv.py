import socket
import struct
import sys

import time

from utils import *
import uuid

from requests import *
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




GID = uuid.uuid4().hex
topInfo = { }

class ConnectionServerHandler(TcpBaseHandler):
    def getGuidForTop(self):
        return GID

    def handleConnection(self, sock, size, buf):
        req = buf.split('*')[0]
        if req == 'PP':
            topId = buf.split('*')[2].strip()
            ip = buf.split('*')[1].split(':')[0]
            port = buf.split('*')[1].split(':')[1]
            if topId not in topInfo.keys():
                topInfo[topId] = Neighbour(ip, int(port), self.getGuidForTop())
            else:
                topInfo[topId].ip = ip
                topInfo[topId].port = int(port)

        if req == GetNeighboursReq.SIG:
            topId = GetNeighboursReq().parse(buf)


            ip, port, gid = topInfo[topId] 
            neighbours = [ ]
            for key in topInfo.keys():
                if topInfo[key].gid == topInfo[topId].gid:
                    neighbours.append(topInfo[key])
                    
            self.request.sendall(GetNeighboursReqA().pkt(neighbours))

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


class ConnectionServerClient(Daemon):
    def __init__(self, ipConnServ, ip, port, ID):
        self.addr = (ipConnServ, CONN_SERV_PORT)
        self.ip = ip
        self.port = port
        self.ID = ID
    def getConnServIP(self):
        # TODO: fix it
        return getSelfIP()
    def getNeighbours(self):
        #TODO
        pass

        
    def main(self):
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.addr)

            pkt = 'PP' + '*'
            pkt += self.ip + ':'
            pkt += str(self.port)
            pkt += '*' + str(self.ID)
            print pkt

            sock.sendall(createPkt(len(pkt), pkt))
            time.sleep(OFFLINE_TIME)



