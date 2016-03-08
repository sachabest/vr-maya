import socket, sys
from PySide import QtCore, QtGui
from maya import cmds, utils
from MayaApp.log.Log import *

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
		self.send_one_frame(self.filenames[0])
		self.send_one_frame(self.filenames[1])


	def send_one_frame(self, filename):
		with open(filename, 'r') as f:
			data = f.read()
		self.sock.send(str(len(data)) + "\n")
		rcv = self.sock.recv(1024).strip()
		if rcv != "k":
			logger.error("Client didn't respond appropriately. Expecting: \"k\". Got: " + rcv);
			self.quit();
		self.sock.send(data)
		rcv = self.sock.recv(1024).strip()
		if rcv != "k":
			logger.error("Client didn't respond appropriately. Expecting: \"k\". Got: " + rcv);
			self.quit();

	def run(self):
		while not self.should_terminate:
			self.send()
		self.sock.close()

	def quit(self):
		self.should_terminate = True

	def blast_background(self):
		utils.executeInMainThreadWithResult(self._blast_background_inner)

	def _blast_background_inner(self):
		cmds.iBlast(filename=self.filenames[0], onscreen=True)
		self.usleep(50)
		cmds.iBlast(filename=self.filenames[1], onscreen=True)
		self.usleep(50)