from PySide.QtCore import *
from PySide.QtGui import *
from MayaApp.ui_main import Ui_MainWindow
from FrameServer.server import FrameServer
from RegistrationServer.server import RegistrationServer
from MayaApp.log.XStream import XStream
from MayaApp.log.Log import *
from MayaApp.scene_creator import Scene
import logging

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
		self.registration_on = False
		XStream.stdout().messageWritten.connect(self.write_info_text)
		XStream.stderr().messageWritten.connect(self.write_error_text)
		self.registration_server = RegistrationServer(self.registered_client, self.bad_register_client)
		self.ui.button_start.clicked.connect(self.start_stop_server)
		self.ui.filename_1.setText(self.filename_1)
		self.ui.filename_2.setText(self.filename_2)
		self.ui.console.setFontPointSize(16)
		self.ui.graphics_1.setScene( QGraphicsScene(0, 0, 250, 200))
		self.ui.graphics_2.setScene( QGraphicsScene(0, 0, 250, 200))
		self.ui.graphics_1.show()
		self.ui.graphics_2.show()
		self.img1 = None
		self.img2 = None

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
		if self.scene:
			self.scene.clean()
			self.scene = None
			print 'Killed Scene'
		event.accept()

	def get_client(self):
		return self.client[0] + ":" + str(self.client[1])

	def registered_client(self, client):
		self.client = client
		logger.info("Registerd client at " + self.get_client())
		self.scene.register_client(client[0])

	def bad_register_client(self, client):
		logger.error("Couldn't register: " + client[0] + ":" + str(client[1]))

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

	def load_images(self, file_1, file_2):
		self.ui.graphics_1.scene().clear()
		self.ui.graphics_2.scene().clear()
		self.img1 = QImage(file_1)
		self.img2 = QImage(file_2)
		self.ui.graphics_1.scene().addPixmap(QPixmap.fromImage(self.img1))
		self.ui.graphics_2.scene().addPixmap(QPixmap.fromImage(self.img2))
		self.ui.graphics_1.scene().setSceneRect(self.img1.rect())
		self.ui.graphics_2.scene().setSceneRect(self.img2.rect())
		self.ui.graphics_1.scene().update()
		self.ui.graphics_2.scene().update()

	def start_stop_server(self):
		if not self.on:
			if self.client is None and not self.registration_on:
				self.registration_on = True
				self.scene = Scene(logger)
				self.start_registration_server()
			elif self.client is None and self.registration_on:
				self.registration_server.quit()
				# self.registration_server = None
				self.registration_on = False
				logger.info("server stopped.")
			else:
				self.server = FrameServer(self.client, (self.filename_1, self.filename_2), (Scene.panel_left, Scene.panel_right))
				# cannot start the server without a client
				self.server.notify_done.connect(self.load_images)
				self.server.start()
				logger.info("Server started.")
				logger.info("Sending frames to " + self.get_client())
				self.on = True
		else:
			self.server.quit()
			self.scene.clean()
			self.scene = None
			self.on = False
			logger1 = logging.getLogger(__name__)
			logger1.info("Server stopped.")