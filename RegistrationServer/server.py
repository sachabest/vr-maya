import SocketServer, sys, logging
from maya import cmds
from PySide.QtCore import *
from MayaApp.log.Log import *

HOST = "localhost"
PORT = 9999

class ServerWrapper(QObject):
    registered = Signal(list)
    bad_registration = Signal(list)
    server = None
        
    def __init__(self, binding, handler):
       QObject.__init__(self)
       self.server = SocketServer.TCPServer(binding, handler)
       self.server.wrapper = self

class MyTCPHandler(SocketServer.BaseRequestHandler):

    in_use = False
    client = None

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = int(self.request.recv(1024).strip())
        if not self.in_use:
            self.client = self.client_address
            self.server.wrapper.registered.emit((self.client[0], self.data))
            self.request.sendall("ok")
        else:
            self.server.wrapper.bad_registration.emit(self.client_address)
            self.request.sendall("no")

class RegistrationServer(QThread):

    wrapper = None

    def __init__(self, success_slot, bad_slot):
        QThread.__init__(self)
        self.daemon = True
        self.wrapper = ServerWrapper((HOST, PORT), MyTCPHandler)
        self.wrapper.registered.connect(success_slot)
        self.wrapper.bad_registration.connect(bad_slot)

    def run(self):
        self.wrapper.server.serve_forever()

    def quit(self):
        self.wrapper.server.shutdown()
        self.wrapper.server.server_close()
        self.wrapper = None