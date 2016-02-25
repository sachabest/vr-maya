# Maya initializer shelf command
# Add this directory to paya python path

import sys
import maya.cmds as cmds

PROJECT_DIR = '/Users/sachabest/Documents/gits/cis099'
PIP_ROOT = '/Applications/Autodesk/maya2016/Maya.app/Contents/MacOS'
COMMAND_NAME = "iBlast.bundle"
COMMAND_PATH = '/Blast/' + COMMAND_NAME

cmds.unloadPlugin(COMMAND_NAME);
cmds.loadPlugin(PROJECT_DIR + COMMAND_PATH);

if PROJECT_DIR not in sys.path:
	sys.path.insert(0, PROJECT_DIR)
	print "Path to project files added to sys.path"

if PIP_ROOT not in sys.path:
	sys.path.insert(0, PIP_ROOT)
	print "Path to pip files added to sys.path"

import RegistrationServer.server
reload(RegistrationServer.server)
import FrameServer.server
reload(FrameServer.server)
import MayaApp.log.Log
reload(MayaApp.log.Log)