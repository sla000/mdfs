import os
import socket
import struct


def getSelfIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def createPkt(len, buf):
    hdr = struct.pack("<ccI", 'm', 'd', len)
    return hdr + buf

class Daemon():
    def __init__(self):
        self.pid = None
    def daemonize(self):
        pid = os.fork()
        if pid == 0:
            try:
                self.main()
            except:
                pass
            finally:
                self.onexit()
        else:
            self.pid = pid
            return pid
    def kill(self):
        os.kill(self.pid, 15)
    def onexit(self):
        pass

    def main(self):
        raise Exception("Not implemented.")

