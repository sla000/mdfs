import socket
import struct
import sys

import time

from utils import *
import uuid

from requests import *
from conserv import CONN_SERV_PORT

def stopTop(ip):
    req = ExitReq()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 8000))
    sock.sendall(req.pkt())
    sock.close()

def stopConnServ(ip):
    req = ExitReq()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, CONN_SERV_PORT))
    sock.sendall(req.pkt())
    sock.close()

if __name__ == '__main__':
    try:
        stopTop(getSelfIP())
    except:
        pass
    try:
        stopConnServ(getSelfIP())
    except:
        pass
