from PySide.QtCore import *
from PySide.QtGui import *
from MayaApp.MainWindow import MainWindow
import maya.OpenMayaUI as mui
import sip

def getMayaWindow():
   '''
   Get the maya main window as a QMainWindow instance
   '''
   ptr = mui.MQtUtil.mainWindow()
   return sip.wrapinstance(long(ptr), QWidget)

window = MainWindow(getMayaWindow())
window.show()