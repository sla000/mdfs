from requests import *
from log import *


class ReqHandler:
    def __init__(self, extra):
        self.reqMap = {
        }
        self.extra = extra
        self.init()
    def init(self):
        pass
    def _register(self, req, handler):
        self.reqMap[req.SIG] = (req, handler)
    def handle(self, buf):
        req = buf.split('*')[0]
        try:
            reqClass, handler = self.reqMap[req]
            args = reqClass.parse(buf)
            log.d('Request: %s, args: %s', req, args)
            handler(*args)
        except KeyError:
            log.e("No such request sig: '%s'", req)

if __name__ == '__main__':
    class T:
        def __init__(self):
            self.a = 2323
        def p(self):
            print self.a


    class ReqHandlerTest(ReqHandler):
        def init(self):
            self._register(ExitReq, self.onExitTest)
        def onExitTest(self, *args):
            self.extra.p()
            print args

    a = T()

    rh = ReqHandlerTest(a)
    rh.handle(ExitReq.create())