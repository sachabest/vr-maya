from maya import cmds, mel
import maya.api.OpenMaya as newMaya
import maya.OpenMaya as oldMaya
import logging

class Scene(object):
    
    panel_left = "modelPanel4"
    panel_right = "modelPanel1"

    def __init__(self, logger):
        self.logger = logger
        self.cam_right = cmds.camera()[0]
        cmds.move(1, 0, 0, self.cam_right)
        self.cam_left = cmds.camera()[0]
        cmds.move(-1, 0, 0, self.cam_left)
        self.mpx_thread = cmds.createNode('transformServer', n='VRTransform')
        cmds.connectAttr(self.mpx_thread + '.outputRotate', self.cam_right + '.rotate')
        cmds.connectAttr(self.mpx_thread + '.outputRotate', self.cam_left + '.rotate')
        mel.eval('setNamedPanelLayout("VR")')
        mel.eval("lookThroughModelPanel " + self.cam_left + " modelPanel4;")
        mel.eval("lookThroughModelPanel " + self.cam_right + " modelPanel1;")
        # self.cube_test = cmds.polyCube(-2, 0, 10)
        # self.sphere_test = cmds.polySphere(2, 0, 10)

    def register_client(self, client):
        cmds.setAttr(self.mpx_thread + '.serverName', client, type="string")
        cmds.setAttr(self.mpx_thread + '.live', True)
        self.logger.info("Configured UDP Server")

    def clean(self):
        cmds.disconnectAttr(self.mpx_thread + '.outputRotate', self.cam_right + '.rotate')
        cmds.disconnectAttr(self.mpx_thread + '.outputRotate', self.cam_left + '.rotate')
        cmds.delete(self.cam_left)
        cmds.delete(self.cam_right)
        cmds.delete(self.mpx_thread)
        # self.logger.info("Cleaned up.")