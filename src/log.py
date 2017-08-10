import logging

LOGGING_LEVEL = logging.DEBUG

class log:
    @staticmethod
    def init(filename):
        logging.basicConfig(format = u'%(levelname)s: %(message)s', level = LOGGING_LEVEL, filename=filename)
    @staticmethod
    def i(*args):
        logging.info(*args)
    @staticmethod
    def d(*args):
        logging.debug(*args)
    @staticmethod
    def e(*args):
        logging.error(*args)
