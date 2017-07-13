from conserv import *
import uuid

topList = { } 

class TopServerHandler(TcpBaseHandler):
    def handleConnection(self, sock, size, buf):
        print 'size = ' + str(size)
        print "buf: " + str(buf)
        ip, port = self.server.server_address
        top = topList[port - 8000]
        


class TopServer(Daemon):
    def __init__(self, ipConnServ, ip, port):
        self.addr = (ip, port)
        Daemon.__init__(self)
        self.ID = uuid.uuid4().hex
        self.connServClient = ConnectionServerClient(ipConnServ, ip, port, self.ID)

    def main(self):
        self.connServClient.daemonize()
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer(self.addr, TopServerHandler)
        server.serve_forever()

class TopServerManager:
    def __init__(self, count):
        self.count = count
    def run(self):
        for i in range(self.count):
            top = TopServer(getSelfIP(), getSelfIP(), 8000 + i)
            top.daemonize()
            topList[i] = top

