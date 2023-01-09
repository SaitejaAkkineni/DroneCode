import cv2
import threading
import numpy as np

class cam():
    def __init__(self,no):
        self.target=[None,None]
        self.VideoSize=[640,480]
        self.camno=no
        self.end=False
        self.frame=None
        t=threading.Thread(target=self.cam)
        t.start()

    def cam(self):
        v=cv2.VideoCapture(self.camno)
        v.set(cv2.CAP_PROP_FRAME_WIDTH, self.VideoSize[0])
        v.set(cv2.CAP_PROP_FRAME_HEIGHT, self.VideoSize[1])
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
        while(True):
            _,self.frame=v.read()
            cv2.rectangle(self.frame,(int((self.VideoSize[0]/2)-50),int((self.VideoSize[1]/2))),(int((self.VideoSize[0]/2)+50),int((self.VideoSize[1]/2)+100)),(0,255,255),2)
            cv2.circle(self.frame, (int(self.VideoSize[0]/2), int((self.VideoSize[1]/2)+50)), 4, (0, 0, 255), -1)
            cv2.imshow("Frame",self.frame)
            out.write(self.frame)
            if cv2.waitKey(1) & 0xFF==ord('q') or self.end==True:
                break
    def arcoDectertor(self,image,ArFound):
        aruco=cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)
        arucoParams = cv2.aruco.DetectorParameters_create()
        corners, ids,_ = cv2.aruco.detectMarkers(image, aruco, parameters=arucoParams)
        if(len(corners)>0):
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                if ArFound==markerID:
                    corners = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))
                    cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                    cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                    cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                    cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
                    self.target[0]=cX=int((topLeft[0] + bottomRight[0]) / 2.0)
                    self.target[1]=cY=int((topLeft[1] + bottomRight[1]) / 2.0)
                    cv2.circle(image,(cX,cY),4,(0,0,255),-1)
                    cv2.putText(image, str(markerID),(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
        return image
    def colorDetector(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        lower = np.array([15, 150, 20])
        upper = np.array([35, 255, 255])
        mask = cv2.inRange(img, lower, upper)
        mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour) > 500:
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    cv2.rectangle(self.image, (x,y), (x + w, y + h), (0, 0, 255), 3)
                    self.target[0]=cX=int(x+w/2)
                    self.target[1]=cY=int(x+h/2)
                    cv2.circle(self.image,(cX,cY),1,(255,0,0),-1)
        return self.image