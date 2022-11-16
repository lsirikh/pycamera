from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class PyCamUi():
    def __init__(self) -> None:
        print("PyCamUi class was created!")
        self.setProperty()
        self.setupUi()
      
    def setProperty(self):
        self.layout= QVBoxLayout()
        self.titleLayout = QVBoxLayout()
        self.viewLayout = QGridLayout()
        self.rtspControlLayout = QGridLayout()
        self.title = QLabel("<font color=red size=20>SENSORWAY CAMERA</font>")
        self.labelRtsp = QLabel()
        self.btnRtsp_start = QPushButton("Camera On")
        self.btnRtsp_stop = QPushButton("Camera Off")
        
        self.controlLayout = QGridLayout()
        self.btnGoLeft = QPushButton("left")
        self.btnGoRight = QPushButton("right")
        self.btnGoUp = QPushButton("up")
        self.btnGoDown = QPushButton("down")
        self.btnGoZoomUp = QPushButton("zoom up")
        self.btnGoZoomOut = QPushButton("zoom out")
        
    def setupUi(self):
        self.titleLayout.addWidget(self.title)
        self.viewLayout.addWidget(self.labelRtsp)
        
        self.rtspControlLayout.addWidget(self.btnRtsp_start, 0,0)
        self.rtspControlLayout.addWidget(self.btnRtsp_stop, 0,1)
        
        self.controlLayout.addWidget(self.btnGoLeft, 1,0)
        self.controlLayout.addWidget(self.btnGoRight, 1,2)
        self.controlLayout.addWidget(self.btnGoUp, 0,1)
        self.controlLayout.addWidget(self.btnGoDown, 2,1)
        self.controlLayout.addWidget(self.btnGoZoomUp, 0,0)
        self.controlLayout.addWidget(self.btnGoZoomOut, 0,2)
        
        self.layout.addLayout(self.titleLayout)
        self.layout.addLayout(self.viewLayout)
        self.layout.addLayout(self.rtspControlLayout)
        self.layout.addLayout(self.controlLayout)