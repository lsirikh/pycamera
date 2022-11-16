import cv2
import threading
import sys
import asyncio

from time import sleep

from Rtsp.RtspService import RtspClass
from Config.JsonService import JsonClass
from Onvif.OnvifService import OnvifClass

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySideConfig.pyside6_uic import *
from Ui.PyCamUi import *

class WindowClass() :
    def __init__(self) :
        #super().__init__()
        print("WindowClass was created!")
        self.setProperty()
        self.setupUi()
        self.btn_connect()
    
    def readConfigData(self, data):
        self.data = data
    
    def setRtspClass(self):
        self.rtsp1.setup(self.data["IR"], self.onvif1.getRtspUri())
        self.rtsp2.setup(self.data["EO"], self.onvif2.getRtspUri())
    
    def setOnvifClass(self):
        self.onvif1.setup(self.data["IR"])
        self.onvif2.setup(self.data["EO"])
        #self.onvif1.getStreamingUrl()
    
    def setProperty(self):
        self.win = QWidget()
        self.layout = QGridLayout()
        self.rtsp1_ui = PyCamUi()
        self.rtsp2_ui = PyCamUi()
        #self.qsize = self.pixmap.size()
        self.rtsp2 = RtspClass()
        self.rtsp2.setLabel(self.rtsp2_ui.labelRtsp)
        self.rtsp1 = RtspClass()
        self.rtsp1.setLabel(self.rtsp1_ui.labelRtsp)
        self.onvif2 = OnvifClass()
        self.onvif1 = OnvifClass()
        self.runningRtsp1 = False
        self.runningRtsp2 = False
        
    def setupUi(self):
        self.layout.addLayout(self.rtsp1_ui.layout, 0,0)
        self.layout.addLayout(self.rtsp2_ui.layout, 0,1)
        self.win.setLayout(self.layout)
        self.win.show()

    def btn_connect(self):
        '''
        RTSP1 on Onvif1 UI Button Connection
        '''
        # self.rtsp1_ui.btnRtsp_start.clicked.connect(self.runRtsp1Thread)
        # self.rtsp1_ui.btnRtsp_stop.clicked.connect(self.stopRtsp1)
        self.rtsp1_ui.btnRtsp_start.clicked.connect(self.rtsp1.startThread)
        self.rtsp1_ui.btnRtsp_stop.clicked.connect(self.rtsp1.stopThread)
        
        self.rtsp1_ui.btnGoLeft.pressed.connect(self.onvif1.moveLeft_pressDonw)
        self.rtsp1_ui.btnGoLeft.released.connect(self.onvif1.btnReleased)
        
        self.rtsp1_ui.btnGoRight.pressed.connect(self.onvif1.moveRight_pressDonw)
        self.rtsp1_ui.btnGoRight.released.connect(self.onvif1.btnReleased)
        
        self.rtsp1_ui.btnGoUp.pressed.connect(self.onvif1.moveUp_pressDonw)
        self.rtsp1_ui.btnGoUp.released.connect(self.onvif1.btnReleased)
        
        self.rtsp1_ui.btnGoDown.pressed.connect(self.onvif1.moveDown_pressDown)
        self.rtsp1_ui.btnGoDown.released.connect(self.onvif1.btnReleased)
        
        self.rtsp1_ui.btnGoZoomUp.pressed.connect(self.onvif1.zoomUp_pressDown)
        self.rtsp1_ui.btnGoZoomUp.released.connect(self.onvif1.btnReleased)
        
        self.rtsp1_ui.btnGoZoomOut.pressed.connect(self.onvif1.zoomOut_pressDown)
        self.rtsp1_ui.btnGoZoomOut.released.connect(self.onvif1.btnReleased)
        
        '''
        RTSP2 on Onvif2 UI Button Connection
        '''
        
        # self.rtsp2_ui.btnRtsp_start.clicked.connect(self.runRtsp2Thread)
        # self.rtsp2_ui.btnRtsp_stop.clicked.connect(self.stopRtsp2)
        self.rtsp2_ui.btnRtsp_start.clicked.connect(self.rtsp2.startThread)
        self.rtsp2_ui.btnRtsp_stop.clicked.connect(self.rtsp2.stopThread)
        
        self.rtsp2_ui.btnGoLeft.pressed.connect(self.onvif2.moveLeft_pressDonw)
        self.rtsp2_ui.btnGoLeft.released.connect(self.onvif2.btnReleased)
        
        self.rtsp2_ui.btnGoRight.pressed.connect(self.onvif2.moveRight_pressDonw)
        self.rtsp2_ui.btnGoRight.released.connect(self.onvif2.btnReleased)
        
        self.rtsp2_ui.btnGoUp.pressed.connect(self.onvif2.moveUp_pressDonw)
        self.rtsp2_ui.btnGoUp.released.connect(self.onvif2.btnReleased)
        
        self.rtsp2_ui.btnGoDown.pressed.connect(self.onvif2.moveDown_pressDown)
        self.rtsp2_ui.btnGoDown.released.connect(self.onvif2.btnReleased)
        
        self.rtsp2_ui.btnGoZoomUp.pressed.connect(self.onvif2.zoomUp_pressDown)
        self.rtsp2_ui.btnGoZoomUp.released.connect(self.onvif2.btnReleased)
        
        self.rtsp2_ui.btnGoZoomOut.pressed.connect(self.onvif2.zoomOut_pressDown)
        self.rtsp2_ui.btnGoZoomOut.released.connect(self.onvif2.btnReleased)
        
        
    
    def onExit(self):
        print("exit")
        self.rtsp1.stopThread()
        self.rtsp2.stopThread()

if __name__ == '__main__':
    try:
        
        app = QApplication([])
        #rtsp = RtspClass()
        jConfig = JsonClass()
        data = jConfig.readConfig()
        window = WindowClass()
        window.readConfigData(data)
        window.setOnvifClass()
        window.setRtspClass()
        
        app.aboutToQuit.connect(window.onExit)
        # Run the main PySide loop
        sys.exit(app.exec())
    except Exception as e:
        print("Raised Exception in __main__ : ", e)