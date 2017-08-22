from slice import *

STORAGE_PATH='storage'
class Storage:
    def __init__(self):
        self.path = STORAGE_PATH
    def put(self, slice):
        dir = os.path.join(self.path, str(slice.hdr.sid)[:2])
        if not os.path.exists(dir):
            os.mkdir(dir)
        filename = os.path.join(dir, str(slice.hdr.sid))
        if os.path.exists(filename):
            return False
        f = open(filename, 'w')
        f.write(slice.buf())
        f.close()
        return True
    def get(self, sid):
        dir = os.path.join(self.path, str(sid)[:2])
        if not os.path.exists(dir):
            return False
        filename = os.path.join(dir, str(sid))
        if os.path.exists(filename):
            return False
        f = open(filename, 'r')
        buf = f.read()
        f.close()
        return Slice.fromFile(buf)
