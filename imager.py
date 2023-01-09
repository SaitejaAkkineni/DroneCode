import cv2
import threading

class cam():
    def __init__(self,no):
        self.target=[None,None]
        self.VideoSize=[640,480]
        t=threading.Thread(target=self.cam)
        self.cam=no
        self.end=False


    def cam(self):
        v=cv2.VideoCapture(self.cam)
        v.set(cv2.CAP_PROP_FRAME_WIDTH, self.VideoSize[0])
        v.set(cv2.CAP_PROP_FRAME_HEIGHT, self.VideoSize[1])
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
        while(True):
            _,frame=v.read()
            frame=self.arucoDetector(frame,1)
            cv2.rectangle(frame,(self.VideoSize[0]/2-50,self.VideoSize[1]/2),(self.VideoSize[0]/2+50,self.VideoSize[1]/2+100),(0,255,255),2)
            cv2.circle(frame, (self.VideoSize[0]/2, self.VideoSize[1]/2+50), 4, (0, 0, 255), -1)
            cv2.imshow("Frame",frame)
            out.write(frame)
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