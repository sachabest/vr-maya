from PySide.QtCore import *
from PySide.QtGui import *
from MayaApp.MainWindow import MainWindow
import maya.OpenMayaUI as mui
from maya import utils
import sip

def getMayaWindow():
   '''
   Get the maya main window as a QMainWindow instance
   '''
   ptr = mui.MQtUtil.mainWindow()
   return sip.wrapinstance(long(ptr), QWidget)

def go():
    window = MainWindow(getMayaWindow())
    window.show()

utils.executeInMainThreadWithResult(go)