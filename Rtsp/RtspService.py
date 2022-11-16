import cv2
import threading
import sys, traceback
import logging
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel

class RtspClass():
    def __init__(self):
        print("RtspClass was created!")
        self.isRtspSet = False
        self.isRtspRun = False
        self.isLabelSet = False
        
    def setup(self, data, rtspUri):
        try:
            ip = data["rtsp"]["ip_address"]
            port = data["rtsp"]["port"]
            id = data["rtsp"]["id"]
            pw = data["rtsp"]["password"]
            self.setNetwork(ip, port)
            self.setAccount(id, pw)
            #head = "rtsp://"+self.ip+":"+str(self.port)
            #url = "rtsp://192.168.1.64:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
            self.url = self.createStreamUrl(rtspUri)
            self.isRtspSet = True
        except:
            print("Raised Exception during setup in RtspClass")
            logging.error(traceback.format_exc())
    
    def setNetwork(self, ip, port):
        self.ip = ip
        self.port = port
    
    def setAccount(self, id, pw):
        self.id = id
        self.__pw = pw
    
    def setOpenCV(self):
        self.cap = cv2.VideoCapture(self.url)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def getDefaultStreamUrl(self):
        return "rtsp://" + self.ip + ":" + str(self.port)
    
    def createStreamUrl(self, rtspUri):
        head = self.getDefaultStreamUrl()
        headWithAuth = "rtsp://"+self.id+":"+self.__pw+"@"+self.ip+":"+str(self.port)
        trailUri = rtspUri.replace(head, "")
        
        return headWithAuth + trailUri
    
    def setLabel(self, label):
        self.label : QLabel = label
        self.isLabelSet = True
    
    def startThread(self):
        try:
            if not self.isLabelSet or self.isRtspRun:
                return
        
            self.isRtspRun = True
            self.rtspThread = threading.Thread(target=self.streaming
                                            , name="[Rtsp streaming {}]".format(self.getDefaultStreamUrl())
                                            )
            self.rtspThread.start()
            print(f"streaming({self.getDefaultStreamUrl()}) started...")
        except Exception as e:
            print("Raised Exception in startTheard : ", e)
        
    def stopThread(self):
        try:
            if not self.isRtspRun:
                return
        
            self.isRtspRun = False
            self.rtspThread.join()
            print(f"streaming({self.getDefaultStreamUrl()}) stoped...")
        except Exception as e:
            print("Raised Exception in stopThread : ", e)
        
    def streaming(self):
        try:
            if self.isRtspSet:
                self.setOpenCV()
            
            while self.isRtspRun:
                    
                ret, img = self.cap.read()
                img = cv2.resize(img, (720, 480))

                if ret:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                    h,w,c = img.shape
                    qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(qImg)
                    self.label.setPixmap(pixmap)
                else:
                    raise Exception("Cannot read frame.")
        
            self.cap.release()
            print(f"streaming({self.getDefaultStreamUrl()}) was finished...")
            
        except Exception as e:
            print("Raised Exception in streaming : ", e)