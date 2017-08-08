class Neighbour:
    def __init__(self, ip, port, gid):
        self.ip = ip
        self.port = port
        self.gid = gid
    def __str__(self):
        return '%s:%u:%s' % (self.ip, self.port, self.gid)
    @staticmethod
    def fromStr(nghStr):
        tmp = nghStr.split(':')
        assert len(tmp) == 3
        ip = tmp[0]
        port = int(tmp[1])
        gid = tmp[2]
        return Neighbour(ip, port, gid)
    
        

        

