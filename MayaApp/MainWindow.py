from PySide.QtCore import *
from PySide.QtGui import *
from MayaApp.ui_main import Ui_MainWindow
from MayaApp.ui_loader import *
from FrameServer.server import FrameServer
from MayaApp.log import Log
from MayaApp.log.XStream import XStream

PROJECT_DIR = '/Users/sachabest/Documents/gits/cis099'

class MainWindow(QMainWindow, Ui_MainWindow):

	server = None
	client = None
	filename_1 = "~/eye1.jpg"
	filename_2 = "~/eye2.jpg"

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		# self.initUI()
		self.setupUi(self)
		# configure stuff here
		self.resize(600, 600)
		self.setWindowTitle("Maya VR")
		self.ui.button_start.clicked.connect(self.start_stop_server)
		self.ui.textFilename1.setText(self.filename_1)
		self.ui.textFilename2.setText(self.filename_2)
		XStream.stdout().messageWritten.connect(self.ui.textConsole.insertPlainText)
		XStream.stderr().messageWritten.connect(self.ui.textConsole.insertPlainText)

	def initUI(self):        
		loader = QUiLoader()        
		currentDir = os.path.dirname(__file__)        
		file = QFile(currentDir+"/mainwindow.ui")        
		file.open(QFile.ReadOnly)        
		self.ui = loader.load(file, parentWidget=self)        
		file.close()

	def set_filename(self, text):
		if self.sender() is self.ui.textFilename1:
			filename_1 = text
		elif self.sender() is self.ui.textFilename2:
			filename_2 = text
		else:
			logger.error("Couldn't match signal to slot.")


	def start_stop_server(self, on):
		if on:
			if client is None or server is None:
				error_msg = QErrorMessage(parent=self)
				error_msg.showMessage("Cannot start the server without a connected client. Please connect one first.")
			else:
				server = FrameServer(client, (filename_1, filename_2))
				# cannot start the server without a client
				server.run()
				logger.info("Server started.")
		else:
			server.quit()
			logger.info("Server stopped.")


	def register_client(self, client):
		self.client = client
		logger.info("Registerd client at " + str(client(0)) + ":" + str(client(1)))