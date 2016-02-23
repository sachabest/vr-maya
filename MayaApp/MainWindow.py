from PySide.QtCore import *
from PySide.QtGui import *
from MayaApp.ui_main import Ui_MainWindow
from FrameServer.server import FrameServer
from RegistrationServer.server import RegistrationServer
from MayaApp.log.XStream import XStream
from MayaApp.log.Log import *

PROJECT_DIR = '/Users/sachabest/Documents/gits/cis099'
COLOR_INFO = QColor("cyan")
COLOR_ERROR = QColor("red")

class MainWindow(QMainWindow):

	server = None
	registration_server = None
	client = None
	filename_1 = PROJECT_DIR + "/eye1.jpg"
	filename_2 = PROJECT_DIR + "/eye2.jpg"
	on = False

	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent=parent)

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		# configure stuff here
		self.resize(600, 600)
		self.setWindowTitle("Maya VR")
		XStream.stdout().messageWritten.connect(self.write_info_text)
		XStream.stderr().messageWritten.connect(self.write_error_text)
		self.registration_server = RegistrationServer(self.registered_client, self.bad_register_client)
		self.ui.button_start.clicked.connect(self.start_stop_server)
		self.ui.filename_1.setText(self.filename_1)
		self.ui.filename_2.setText(self.filename_2)

	def start_registration_server(self):
		self.registration_server.start()
		logger.info("Started registration server. Awaiting device connections.")

	def closeEvent(self, event):
		if self.registration_server:
			self.registration_server.quit()
			self.registration_server = None
			print "Killed Registration Server"
		if self.server:
			self.server.quit()
			self.server = None
			print "Killed Frame Server"

	def registered_client(self, client):
		self.client = client
		logger.info("Registered: " + client)

	def bad_register_client(self, client):
		self.write_error_text("Couldn't register: " + client(0) + ":" + str(client(1)))

	def write_error_text(self, text):
		self.ui.console.setTextColor(COLOR_ERROR)
		self.ui.console.insertPlainText(text)

	def write_info_text(self, text):
		self.ui.console.setTextColor(COLOR_INFO)
		self.ui.console.insertPlainText(text)

	def set_filename(self, text):
		if self.sender() is self.ui.textFilename1:
			self.filename_1 = text
		elif self.sender() is self.ui.textFilename2:
			self.filename_2 = text
		else:
			logger.error("Couldn't match signal to slot.")


	def blast_manual(self):
		self.server = FrameServer(('localhost', 9999), (self.filename_1, self.filename_2))
		self.server.run()
		logger.info("Server started.")
		self.on = True

	def start_stop_server(self):
		if not self.on:
			if self.client is None:
				self.start_registration_server()
				# error_msg = QErrorMessage(parent=self)
				# error_msg.showMessage("Cannot start the server without a connected client. Please connect one first.")
			else:
				self.server = FrameServer(self.client, (self.filename_1, self.filename_2))
				# cannot start the server without a client
				self.server.start()
				logger.info("Server started.")
				self.on = True
		else:
			self.server.quit()
			self.on = False
			logger.info("Server stopped.")


	def register_client(self, client):
		self.client = client
		logger.info("Registerd client at " + str(client(0)) + ":" + str(client(1)))