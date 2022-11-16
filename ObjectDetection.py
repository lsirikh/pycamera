import time
import numpy as np
import cv2
import torch
import torch.backends.cudnn as cudnn
from models.experimental import attempt_load
from utils.general import non_max_suppression



camera = 0
#$path = 'C:\Users\Sensorway\source\python\AICamera\yolov5'
#path = ""
#weight = f'{path}\yolov5s.pt'
weight = "./yolov5s.pt"
device = torch.device('cpu')

model = attempt_load(weights = weight, device=device)
stride = int(model.stride.max())
cudnn.benchmark = True

cap = cv2.VideoCapture("rtsp://admin:Abc.12345@192.168.1.64:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif")

#width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
width = 352
#height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
height = 288

cap.set(3, width)
cap.set(4, height)

while(cap.isOpened()):
    time.sleep(0.2)
    ret, frame = cap.read()
    if ret == True:
        now = time.time()
        img = cv2.resize(frame, (720, 480))
        img = torch.from_numpy(frame).float().to(device).permute(2,0,1)
        img /= 255.0
        
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        
        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.39, 0.45, classes=0, agnostic=True)
        print('time -> ', time.time() - now)
        
        for det in pred:
            if len(det):
                print(det)
                time_stamp = int(time.time())
                fcm_photo = f'./detected/{time_stamp}.png'
                cv2.imwrite(fcm_photo, frame)
                time.sleep(1)
    else:
        break;
    
cap.release()            
