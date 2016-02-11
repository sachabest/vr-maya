from PySide.QtCore import *
from PySide.QtGui import *
from MayaApp.ui_main import Ui_MainWindow
from FrameServer.server import FrameServer
from RegistrationServer.server import RegistrationServer
from MayaApp.log import Log
from MayaApp.log.XStream import XStream

PROJECT_DIR = '/Users/sachabest/Documents/gits/cis099'
COLOR_INFO = QColor("cyna")
COLOR_ERROR = QColor("red")

class MainWindow(QMainWindow):

	server = None
	registration_server = None
	client = None
	filename_1 = "~/eye1.jpg"
	filename_2 = "~/eye2.jpg"
	on = False

	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent=parent)

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		# configure stuff here
		self.resize(600, 600)
		self.setWindowTitle("Maya VR")
		self.registration_server = RegistrationServer(self.registered_client, self.bad_register_client)
		self.ui.button_start.clicked.connect(self.start_stop_server)
		self.ui.filename_1.setText(self.filename_1)
		self.ui.filename_2.setText(self.filename_2)
		XStream.stdout().messageWritten.connect(self.write_info_text)
		XStream.stderr().messageWritten.connect(self.write_error_text)


	def closeEvent(self, event):
		if registration_server:
			registration_server.quit()
			registration_server = None
		if server:
			server.quit()
			server = None

	def registered_client(self, client):
		self.client = client
		self.write_info_text("Registered: " + client(0) + ":" + str(client(1)))

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
			filename_1 = text
		elif self.sender() is self.ui.textFilename2:
			filename_2 = text
		else:
			logger.error("Couldn't match signal to slot.")


	def start_stop_server(self):
		if not self.on:
			if self.client is None or server is None:
				error_msg = QErrorMessage(parent=self)
				error_msg.showMessage("Cannot start the server without a connected client. Please connect one first.")
			else:
				self.server = FrameServer(client, (filename_1, filename_2))
				# cannot start the server without a client
				self.server.run()
				logger.info("Server started.")
				self.on = True
		else:
			self.server.quit()
			self.on = False
			logger.info("Server stopped.")


	def register_client(self, client):
		self.client = client
		logger.info("Registerd client at " + str(client(0)) + ":" + str(client(1)))