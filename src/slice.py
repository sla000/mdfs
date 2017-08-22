import os
import tempfile

import shutil

import struct
import uuid

GFSPLIT_PATH='./libgfshare/gfsplit'
GFCOMBINE_PATH='./libgfshare/gfcombine'

GUID_SIZE = 32
class SliceHdr:
    def __init__(self, nkInfo, sid, fid):
        self.nkInfo = nkInfo
        self.sid = sid
        self.fid = fid
        # format sizeOfNkInfo + nkInfo + sid + fid

    def buf(self):
        size = struct.pack('<I', len(str(self.nkInfo)))
        return size + self.nkInfo + self.sid + self.fid

    @staticmethod
    def fromFile(filename, sid=uuid.uuid4().hex, fid=uuid.uuid4().hex):
        nkInfo = filename.split('.')[-1]
        return SliceHdr(nkInfo, sid, fid)
    @staticmethod
    def fromBuf(buf):
        size = struct.unpack('<I', buf[:4])
        buf = buf[4:]
        nkInfo = buf[:size]
        buf = buf[size:]
        sid = buf[:GUID_SIZE]
        buf = buf[GUID_SIZE:]
        fid = buf[:GUID_SIZE]
        assert len(buf) == GUID_SIZE
        size = 4 + size + GUID_SIZE + GUID_SIZE
        return size, SliceHdr(nkInfo, sid, fid)


class Slice:
    def __init__(self, hdr, body):
        self.hdr = hdr
        self.body = body
        self.slice = hdr.buf() + body
    @staticmethod
    def fromFile(filename):
        basename = os.path.join(filename)
        f = open(filename, 'r')
        body = f.read()
        f.close()
        return Slice(SliceHdr.fromFile(basename), body
    @staticmethod
    def fromBuf(buf):
        hdrSize, hdr = SliceHdr.fromBuf(buf)
        body = buf[hdrSize:]
        return Slice(hdr, bodygit



class SliceManager:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.slices = [ ]
    def split(self, filename):
        assert len(self.slices) == 0, 'SliceManager use only one time per operation'
        tempdir = tempfile.mkdtemp()
        cwd = os.getcwd()

        copiedFile = os.path.join(tempdir, os.path.basename(filename))
        shutil.copyfile(filename, copiedFile)
        assert os.path.exists(copiedFile)


        os.system('%s -n %i -m %s %s' % (GFSPLIT_PATH, self.k, self.n, copiedFile))

        sliceFiles = filter(lambda x: x != os.path.basename(copiedFile), os.listdir(tempdir))
        sliceFiles = map(lambda x: os.path.join(tempdir, x), sliceFiles)

        for sliceFile in sliceFiles:
            self.appendSlice(Slice.fromFile(sliceFile))
    def appendSlice(self, sliceBuf):
        self.slices.append(sliceBuf)

    def combine(self, filename):
        #TODO: fix it
        assert len(self.slices) >= self.k, 'SliceManager combine operation: too few slices for combine. Use appendSlice %i times.' % self.k
        tempdir = tempfile.mkdtemp()


        sliceFIles = map(lambda x: os.path.join(tempdir, 'temp.%03i' % x), range(self.k))
        print sliceFIles




        for i, file in enumerate(sliceFIles):
            f = open(file, 'wb')
            f.write(self.slices[i])
            f.close()


        cmd = '%s -o %s ' % (GFCOMBINE_PATH, filename)
        for i in range(self.k):
            cmd += sliceFIles[i] + ' '
        print cmd
        os.system(cmd)


if __name__ == '__main__':
    sm = SliceManager(10, 2)

    temp = tempfile.mktemp()
    print os.path.basename(temp)
    f = open(temp, 'w')
    f.write('Test data.\n')
    f.close()

    sm.split(temp)
    #sm.combine('temp')
