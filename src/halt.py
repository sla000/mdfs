import socket
import struct
import sys

import time

from utils import *
import uuid

from requests import *
from conserv import CONN_SERV_PORT

def stopTop(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 8000))
    sock.sendall(ExitReq.pkt())
    sock.close()

def stopConnServ(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, CONN_SERV_PORT))
    sock.sendall(ExitReq.pkt())
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
