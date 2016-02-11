import SocketServer, sys, logging
from maya import cmds
from PySide.QtCore import *

HOST = "localhost"
PORT = 9999

class MyTCPHandler(SocketServer.BaseRequestHandler):

    in_use = False
    client = None

    registered = Signal(str)
    bad_registration = Signal(str)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        if not self.in_use:
            client = self.client_address
            self.registered.emit(self.client)
            self.request.sendall("ok")
        else:
            self.bad_registration.emit(self.client_address)
            self.request.sendall("no")

class RegistrationServer(QThread):

    sock = None

    def __init__(self, success_slot, bad_slot):
        self.daemon = True
        self.sock = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
        self.sock.registered.connect(success_slot)
        self.sock.bad_registration.connect(bad_slot)

    def run(self):
        self.sock.serve_forever()

    def quit(self):
        self.sock.shutdown()
        self.sock.server_close()
        self.sock = None