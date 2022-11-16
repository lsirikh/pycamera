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
        self.rtsp1 = RtspClass()
        self.rtsp1.setLabel(self.rtsp1_ui.labelRtsp)
        self.rtsp2 = RtspClass()
        self.rtsp2.setLabel(self.rtsp2_ui.labelRtsp)
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
        
        
    def runFirst(self):
        self.rtsp1.setup(self.data["IR"], self.onvif1.getRtspUri())
        
        try:
            while self.runningRtsp1:
                    
                ret, img = self.rtsp1.cap.read()
                img = cv2.resize(img, (720, 480))
                # size = self.labelRtsp1.width(), self.labelRtsp1.height()
                # print(size[0], size[1])
                # img = cv2.resize(img, size)
                if ret:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                    h,w,c = img.shape
                    qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(qImg)
                    self.rtsp1_ui.labelRtsp.setPixmap(pixmap)
                else:
                    QMessageBox.about(self.win, "Error", "Cannot read frame.")
                    print("cannot read frame.")
                    break
        
            self.rtsp1.cap.release()
            print("RTSP1 Thread end.")
        except Exception as e:
            print("Raised Exception in runFirst : ", e)

            
    def runRtsp1Thread(self):
        if self.runningRtsp1:
            return
        
        self.runningRtsp1 = True
        self.rtspThread1 = threading.Thread(target=self.runFirst)
        self.rtspThread1.start()
        print("RTSP1 started..")
    
    def stopRtsp1(self):
        if not self.runningRtsp1:
            return
        
        self.runningRtsp1 = False
        self.rtspThread1.join()
        print("RTSP1 stoped..")
          
    def runSecond(self):
        self.rtsp2.setup(self.data["EO"], self.onvif2.getRtspUri())
        
        try:
            while self.runningRtsp2:
                ret, img = self.rtsp2.cap.read()
                img = cv2.resize(img, (720, 480))
                #img = cv2.resize(img, (self.labelRtsp2.width(), self.labelRtsp2.height()))
                
                if ret:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                    h,w,c = img.shape
                    qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(qImg)
                    self.rtsp2_ui.labelRtsp.setPixmap(pixmap)
                else:
                    QMessageBox.about(self.win, "Error", "Cannot read frame.")
                    print("cannot read frame.")
                    break
                
            self.rtsp2.cap.release()
            print("RTSP2 Thread end.")
        except Exception as e:
            print("Raised Exception in runSecond : ", e)

            
    def runRtsp2Thread(self):
        if self.runningRtsp2:
            return
        
        self.runningRtsp2 = True
        self.rtspThread2 = threading.Thread(target=self.runSecond)
        self.rtspThread2.start()
        print("RTSP2 started..")
    
    def stopRtsp2(self):
        if not self.runningRtsp2:
            return
        
        self.runningRtsp2 = False
        self.rtspThread2.join()
        print("RTSP2 stoped..")
        
        
    # def goLeft(self):
    #     self.loop = getattr(self, 'loop', asyncio.get_event_loop())
    #     self.loop.run_until_complete(self.onvif.move_left(0.1))
    
    # def goRight(self):
    #     self.loop = getattr(self, 'loop', asyncio.get_event_loop())
    #     self.loop.run_until_complete(self.onvif.move_right(0.1))
    
    # def goUp(self):
    #     self.loop = getattr(self, 'loop', asyncio.get_event_loop())
    #     self.loop.run_until_complete(self.onvif.move_up(0.1))
        
    # def goDown(self):
    #     self.loop = getattr(self, 'loop', asyncio.get_event_loop())
    #     self.loop.run_until_complete(self.onvif.move_down(0.1))
    
    # def goZoomUp(self):
    #     self.loop = getattr(self, 'loop', asyncio.get_event_loop())
    #     self.loop.run_until_complete(self.onvif.zoom_up(0.1))
    
    # def goZoomOut(self):
    #     self.loop = getattr(self, 'loop', asyncio.get_event_loop())
    #     self.loop.run_until_complete(self.onvif.zoom_dowm(0.1))        

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