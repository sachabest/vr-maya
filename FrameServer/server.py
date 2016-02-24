import socket, sys
from PySide import QtCore, QtGui
from maya import cmds, utils

HOST = "localhost"
PORT = 9998

class FrameServer(QtCore.QThread):

	sock = None
	destination = None
	filenames = None
	should_terminate = False

	def __init__(self, destination, filenames):
		QtCore.QThread.__init__(self)
		self.daemon = True
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.destination = destination
		self.sock.connect(self.destination)
		self.filenames = filenames

	def send(self):
		self.blast_background()
		with open(self.filenames[0], 'r') as f:
			data = f.read()
			self.sock.send(data + '\n')
		self.sock.recv(8)
		with open(self.filenames[1], 'r') as f:
			data = f.read()
			self.sock.send(data + '\n')
		self.sock.recv(8)

	def run(self):
		while not self.should_terminate:
			self.send()
		self.sock.close()

	def quit(self):
		self.should_terminate = True

	def blast_background(self):
		utils.executeInMainThreadWithResult(self._blast_background_innter)

	def _blast_background_innter(self):
		cmds.iBlast(filename=self.filenames[0], onscreen=True)
		cmds.iBlast(filename=self.filenames[1], onscreen=True)
