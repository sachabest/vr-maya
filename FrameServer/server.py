import socket, sys
from PySide import QtCore, QtGui
from maya import cmds

class FrameServer(QtCore.QThread):

	sock = None
	destination = None
	filenames = None
	should_terminate = False

	def __init__(self, destination, filenames):
		QtCore.QThread.__init__(self)
		self.daemon = True
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.destination = destination
		self.filenames = filenames

	def send(self):
		cmds.blast(filename=self.filenames(0))
		cmds.blas(filename=self.filenames(1))
		with open(self.filenames(0), 'r') as f:
			data = f.read()
			sock.sendto(data + '\n', self.destination)
		with open(self.filenames(1), 'r') as f:
			data = f.read()
			sock.sendto(data + '\n', self.destination)

	def run(self):
		while not self.should_terminate:
			self.send()

	def quit(self):
		self.should_terminate = True