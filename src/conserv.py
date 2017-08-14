from reqhandler import  *
from net import *
from db import *

OFFLINE_TIME = 5
CONN_SERV_PORT=4545


GID = uuid.uuid4().hex
topInfo = { }
class ConnectionServerReqHandler(ReqHandler):
    def init(self):
        map = {
            ExitReq : self.onExit,
            TopServerOnlineReq : self.onTopServerOnline,
            GetNeighboursReq : self.onGetNeighbours,
            GetFileIDReq : self.onGetFileID
        }

        for key in map.keys():
            self._register(key, map[key])
    def __sendResponcePkt(self, requestClass, *args):

        self.extra.request.sendall(requestClass.pkt(args))
    def onExit(self):
        log.i('onExit')
        self.extra.stop()
    def onTopServerOnline(self, ip, port, topId):
        log.i('Top %s is online' % ip)
        if topId not in topInfo.keys():
            topInfo[topId] = Neighbour(ip, int(port), self.extra.getGuidForTop())
        else:
            topInfo[topId].ip = ip
            topInfo[topId].port = int(port)
    def onGetNeighbours(self, topId):
        neighbours = [ ]
        for key in topInfo.keys():
            if topInfo[key].gid == topInfo[topId].gid and key != topId:
                neighbours.append(topInfo[key])

        log.i(neighbours)
        log.i(GetNeighboursReqA.pkt(neighbours))
        self.__sendResponcePkt(GetNeighboursReqA, neighbours)
        #self.__sendResponcePkt(GetNeighboursReqA.pkt(neighbours))
    def onGetFileID(self, fileHash):
        db = ConnServDb()
        fileID = db.getFileID(fileHash)
        log.d('Got file ID [%s]. FileID = %s', fileHash, fileID)
        self.__sendResponcePkt(GetFileIDResp, fileID)
        #self.__sendResponcePkt(GetFileIDResp.pkt(fileID))

class ConnectionServerHandler(TcpBaseHandler):

    def getGuidForTop(self):
        return GID

    def handleConnection(self, sock, size, buf):
        reqHandler = ConnectionServerReqHandler(self)
        reqHandler.handle(buf)

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
        sock = getConnectedSock(self.addr[0], self.addr[1])
        sendPkt(sock,  GetNeighboursReq.pkt(self.ID))
        
        buf = recvPkt(sock)
        nlist = GetNeighboursReqA.parse(buf)
        log.i('nlist = %s', str(nlist))
        sock.close()
        return nlist
    def getFileID(self, fileHash):
        ip, port = self.addr
        sock = getConnectedSock(ip, port)
        sendPkt(sock, GetFileIDReq.pkt(fileHash))
        buf = recvPkt(sock)
        fileID = GetFileIDResp.parse(buf)
        sock.close()
        log.d('GetFileIDReq: sended hash [%s], got FileID = %s', fileHash, fileID)
        return fileID

    def main(self):
        while self.work:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(self.addr)
                sock.sendall(TopServerOnlineReq.pkt(self.ip, self.port, self.ID))
                time.sleep(OFFLINE_TIME)
            except Exception as e:
                log.e('ConnectionServerClient.main: ' + e.__class__ + ' ' + e.message)


if __name__ == '__main__':
    log.init('/tmp/connserv.log')
    s = ConnectionServer()
    s.start()