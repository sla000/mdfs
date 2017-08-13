import socket
import struct
import sys

import time

from net import *
from utils import *
import uuid
from log import *
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
        if req == TopServerOnlineReq.SIG:
            ip, port, topId = TopServerOnlineReq().parse(buf)
            if topId not in topInfo.keys():
                topInfo[topId] = Neighbour(ip, int(port), self.getGuidForTop())
            else:
                topInfo[topId].ip = ip
                topInfo[topId].port = int(port)
            log.i('Top %s is online' % ip)

        if req == GetNeighboursReq.SIG:
            topId = GetNeighboursReq().parse(buf)

            neighbours = [ ]
            for key in topInfo.keys():
                if topInfo[key].gid == topInfo[topId].gid and key != topId:
                    neighbours.append(topInfo[key])
                    
            log.i(neighbours)
            log.i(GetNeighboursReqA().pkt(neighbours))
            self.request.sendall(GetNeighboursReqA().pkt(neighbours))

        if req == ExitReq.SIG:
            self.stop()
    def stop(self):
        log.i('stopping')
        self.server.server_close()
        os._exit(0)

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


class ConnectionServerClient:
    def __init__(self, ipConnServ, ip, port, ID):
        self.addr = (ipConnServ, CONN_SERV_PORT)
        self.ip = ip
        self.port = port
        self.ID = ID
        self.pid = -1
        self.work = False

    def start(self):
        pid = os.fork()
        if pid == 0:
            self.work = True
            self.main()
        elif pid > 0:
            self.pid = pid

    def stop(self):
        assert self.work == True
        self.work = False

    def getNeighbours(self):
        req = GetNeighboursReq()

        sock = getConnectedSock(self.addr[0], self.addr[1])
        sendPkt(sock, req.pkt(self.ID))
        
        buf = recvPkt(sock)
        nlist = GetNeighboursReqA().parse(buf)
        log.i('nlist = %s', str(nlist))
        return nlist
        
    def main(self):
        while self.work:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(self.addr)
                sock.sendall(TopServerOnlineReq().pkt(self.ip, self.port, self.ID))
                time.sleep(OFFLINE_TIME)
            except Exception as e:
                log.e('ConnectionServerClient.main: ' + e.message)


if __name__ == '__main__':
    log.init('/tmp/connserv.log')
    s = ConnectionServer()
    s.start()
