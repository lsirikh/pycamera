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
        self.layout = QVBoxLayout()
        self.titleLayout = QVBoxLayout()
        self.viewLayout = QGridLayout()
        self.rtspControlLayout = QGridLayout()
        self.title = QLabel("<font color=red size=40>SENSORWAY CAMERA</font>")
        self.labelRtsp1 = QLabel()
        self.labelRtsp2 = QLabel()
        self.btnRtsp1_start = QPushButton("Camera On")
        self.btnRtsp1_stop = QPushButton("Camera Off")
        
        self.btnRtsp2_start = QPushButton("Camera On")
        self.btnRtsp2_stop = QPushButton("Camera Off")
        
        self.pixmap = QPixmap('\\resources\\turnoff_video.png')
        
        self.controlLayout = QGridLayout()
        self.btnGoLeft = QPushButton("left")
        self.btnGoRight = QPushButton("right")
        self.btnGoUp = QPushButton("up")
        self.btnGoDown = QPushButton("down")
        self.btnGoZoomUp = QPushButton("zoom up")
        self.btnGoZoomOut = QPushButton("zoom out")
        
        self.qsize = self.pixmap.size()
        self.rtsp1 = RtspClass()
        self.rtsp2 = RtspClass()
        self.onvif2 = OnvifClass()
        self.onvif1 = OnvifClass()
        self.runningRtsp1 = False
        self.runningRtsp2 = False
        
    def setupUi(self):
        print("image size h: {} w: {}".format(self.pixmap.height(), self.pixmap.width()))
        self.labelRtsp1.setPixmap(self.pixmap)
        
        self.titleLayout.addWidget(self.title)
        self.viewLayout.addWidget(self.labelRtsp1, 1,0)
        self.viewLayout.addWidget(self.labelRtsp2, 1,1)
        
        self.rtspControlLayout.addWidget(self.btnRtsp1_start, 0,0)
        self.rtspControlLayout.addWidget(self.btnRtsp1_stop, 0,1)
        self.rtspControlLayout.addWidget(self.btnRtsp2_start, 0,2)
        self.rtspControlLayout.addWidget(self.btnRtsp2_stop, 0,3)
        
        self.controlLayout.addWidget(self.btnGoLeft, 1,0)
        self.controlLayout.addWidget(self.btnGoRight, 1,2)
        self.controlLayout.addWidget(self.btnGoUp, 0,1)
        self.controlLayout.addWidget(self.btnGoDown, 2,1)
        self.controlLayout.addWidget(self.btnGoZoomUp, 0,0)
        self.controlLayout.addWidget(self.btnGoZoomOut, 0,2)
        
        #self.parentGridLayout.addLayout(self.gridLayout, 3,0, 3,2)
        self.layout.addLayout(self.titleLayout)
        self.layout.addLayout(self.viewLayout)
        self.layout.addLayout(self.rtspControlLayout)
        self.layout.addLayout(self.controlLayout)
        self.win.setLayout(self.layout)
        self.win.show()

    def btn_connect(self):
        self.btnRtsp1_start.clicked.connect(self.runRtsp1Thread)
        self.btnRtsp1_stop.clicked.connect(self.stopRtsp1)
        self.btnRtsp2_start.clicked.connect(self.runRtsp2Thread)
        self.btnRtsp2_stop.clicked.connect(self.stopRtsp2)
        
        self.btnGoLeft.pressed.connect(self.onvif2.moveLeft_pressDonw)
        self.btnGoLeft.released.connect(self.onvif2.btnReleased)
        
        self.btnGoRight.pressed.connect(self.onvif2.moveRight_pressDonw)
        self.btnGoRight.released.connect(self.onvif2.btnReleased)
        
        self.btnGoUp.pressed.connect(self.onvif2.moveUp_pressDonw)
        self.btnGoUp.released.connect(self.onvif2.btnReleased)
        
        self.btnGoDown.pressed.connect(self.onvif2.moveDown_pressDown)
        self.btnGoDown.released.connect(self.onvif2.btnReleased)
        
        self.btnGoZoomUp.pressed.connect(self.onvif2.zoomUp_pressDown)
        self.btnGoZoomUp.released.connect(self.onvif2.btnReleased)
        
        self.btnGoZoomOut.pressed.connect(self.onvif2.zoomOut_pressDown)
        self.btnGoZoomOut.released.connect(self.onvif2.btnReleased)
        
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
                    self.labelRtsp1.setPixmap(pixmap)
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
                    self.labelRtsp2.setPixmap(pixmap)
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
        self.stopRtsp1()
        self.stopRtsp2()

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