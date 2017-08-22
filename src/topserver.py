from conserv import *
import uuid
from log import *
from config import *
from storage import *

class Top:
    def __init__(self):
        self.a = 1

gTop = Top()

class TopServerReqHandler(ReqHandler):
    def init(self):
        map = {
            ExitReq : self.onExit,
            AddSliceReq : self.addSlice
        }

        for key in map.keys():
            self._register(key, map[key])

    def onExit(self):
        log.i('onExit')
        self.extra.stop()
    def addSlice(self, sliceBuf):
        log.i('AddSliceReq')
        slice = Slice.fromBuf(sliceBuf)
        storage = Storage()
        if storage.put(slice) == False:
            log.i('Slice %s already exists in storage' % str(slice.hdr.sid))



class TopServerHandler(TcpBaseHandler):
    def handleConnection(self, sock, size, buf):
        reqHandler = TopServerReqHandler()
        reqHandler.handle(buf)

    def stop(self):
        log.i('stopping')
        self.server.server_close()
        self.server.connServClient.stop()
        os._exit(0)

class TopServer(Daemon):
    def __init__(self, ipConnServ, ip, port):
        self.addr = (ip, port)
        Daemon.__init__(self)
        self.ID = uuid.uuid4().hex
        self.connServClient = ConnectionServerClient(ipConnServ, ip, port, self.ID)

    def main(self):
        log.i('TopServer.main')
        self.connServClient.start()
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer(self.addr, TopServerHandler)
        server.serve_forever()

if __name__ == '__main__':
    log.init('/tmp/topserver.log')
    top = TopServer(CONN_SERV_IP, getSelfIP(), 8000)
    top.start()
