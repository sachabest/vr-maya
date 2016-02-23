import logging
from XStream import XStream
class QtHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
    def emit(self, record):
        record = self.format(record)
        if record:
        	XStream.stdout().write('%s\n'%record)