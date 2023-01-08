import cv2
import numpy as np
from heightControl import *
from time import *
from Drone import Drone

VBSize=[640,480]
VBCenter=[int(VBSize[0]/2),int(VBSize[1]/2)] 
ArCenter=[-1,-1]  
ColCenter=[-1,-1]
ArValue=1
foundValue=-1
ArFound=False
ColFound=False


def colorDetector(image):
    global ColCenter
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([15, 150, 20])
    upper = np.array([35, 255, 255])
    mask = cv2.inRange(img, lower, upper)
    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(image, (x,y), (x + w, y + h), (0, 0, 255), 3)
                ColCenter[0]=cX=int(x+w/2)
                ColCenter[1]=cY=int(x+h/2)
                cv2.circle(image,(cX,cY),1,(255,0,0),-1)
    return image

def arucoDetector(image,value):
    global ArCenter,ArFound,foundValue
    aruco=cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)
    arucoParams = cv2.aruco.DetectorParameters_create()
    corners, ids,_ = cv2.aruco.detectMarkers(image, aruco, parameters=arucoParams)
    if(len(corners)>0):
        ids = ids.flatten()
        for (markerCorner, markerID) in zip(corners, ids):
            foundValue=markerID
            if True:
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
                ArCenter[0]=cX=int((topLeft[0] + bottomRight[0]) / 2.0)
                ArCenter[1]=cY=int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(image,(cX,cY),4,(0,0,255),-1)
                cv2.putText(image, str(markerID),(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
    return image

def camCapture(no):
    global VBSize,ArFound,ArCenter,ArValue,ColFound,foundValue
    vi=cv2.VideoCapture(no)
    vi.set(cv2.CAP_PROP_FRAME_WIDTH, VBSize[0])
    vi.set(cv2.CAP_PROP_FRAME_HEIGHT, VBSize[1])
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    while(True):
        _,frame=vi.read()
        frame=arucoDetector(frame,ArValue)
        cv2.rectangle(frame,(VBCenter[0]-50,VBCenter[1]),(VBCenter[0]+50,VBCenter[1]+100),(0,255,255),2)
        cv2.circle(frame, (VBCenter[0], VBCenter[1]+50), 4, (0, 0, 255), -1)
        cv2.imshow("Frame",frame)
        out.write(frame)
        if(ArFound and ArValue==foundValue):
            ArCenter[0],ArCenter[1]=(ArCenter[0]-VBCenter[0])*(255/VBCenter[0]),(ArCenter[1]-VBCenter[1])*(255/VBSize[1])
            cv2.putText(image, str(markerID),(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
            if(abs(ArCenter[0])>50 or abs(ArCenter[1])>50):
                if(ArCenter[0]>0 and ArCenter[1]>0):
                    Drone.control('r')
                elif(ArCenter[0]<0 and ArCenter[1]>0):
                    Drone.control('a')
                elif(ArCenter[0]<0 and ArCenter[1]<0):
                    Drone.control('s')
                else:
                    Drone.control('f')
            else:
                # turn on/off magnet command
                mantainAlt(5)
                sleep(10)
                mantainAlt(100)
                continue
            ArValue=0
        elif(ColFound):
            ColCenter[0],ColCenter[1]=(ColCenter[0]-VBCenter[0])*(255/VBCenter[0]),(ColCenter[1]-VBCenter[1])*(255/VBCenter[1])
            if(abs(ColCenter[0])>50 or abs(ColCenter[1])>50):
                if(ColCenter[0]>0 and ColCenter[1]>0):
                    Drone.control('r')
                    continue
                elif(ColCenter[0]<0 and ColCenter[1]>0):
                    # Move left to Arcenter
                    continue
                elif(ColCenter[0]<0 and ColCenter[1]<0):
                    # Move backward to Arcenter
                    continue
                else:
                    # Move right to ArCenter
                    continue
            else:
                #turn on/off magnet command
                mantainAlt(5)
                sleep(10)
                mantainAlt(100)
                sleep(5)
            ArValue=0
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break


if __name__=="__main__":
#     mantainAlt(100)
    camCapture(0)
