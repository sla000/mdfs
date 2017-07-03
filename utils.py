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
    def daemonize(self):
        pid = os.fork()
        if pid == 0:
            self.main()
        else:
            return pid



    def main(self):
        raise Exception("Not implemented.")

