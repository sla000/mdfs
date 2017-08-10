from conserv import *
import uuid
from log import *
from config import *


class Top:
    def __init__(self):
        self.a = 1

gTop = Top()

class TopServerHandler(TcpBaseHandler):
    def handleConnection(self, sock, size, buf):
        log.i('size = ' + str(size))
        log.i("buf: " + str(buf))
        ip, port = self.server.server_address

        req = buf.split('*')[0]
        if req == ExitReq.SIG:
            self.stop()
    def stop(self):
        log.i('stopping')
        self.server.server_close()
        os._exit(0)

class TopServer(Daemon):
    def __init__(self, ipConnServ, ip, port):
        self.addr = (ip, port)
        Daemon.__init__(self)
        self.ID = uuid.uuid4().hex
        self.connServClient = ConnectionServerClient(ipConnServ, ip, port, self.ID)

    def main(self):
        log.i('TopServer.main')
        self.connServClient.daemonize()
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer(self.addr, TopServerHandler)
        server.serve_forever()

if __name__ == '__main__':
    log.init('/tmp/topserver.log')
    top = TopServer(CONN_SERV_IP, getSelfIP(), 8000)
    top.daemonize()
