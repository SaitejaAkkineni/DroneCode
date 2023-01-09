from heightControl import HeightController
from imager import cam
from movement import movement
from distance import distance
from time import sleep

def pickDrop(droppoint):
    move.moveto(camera.target)
    heightControl.height=10
    sleep(5)
    #magnet command
    heightControl.height=100
    camera.arcoDectertor(camera.frame,droppoint)
    move.moveto(camera.target)
    heightControl.height=10
    sleep(5)
    #magnet command
    heightControl.height=100

if __name__=="__main__":
    heightControl=HeightController(100)
    camera=cam(0)
    move=movement()
    camera.arcoDectertor(camera.frame,11)
    move.moveto(camera.target)
    heightControl.height=10
    sleep(5)
    #magnet command
    heightControl.height=100
    camera.arcoDectertor(camera.frame,0)
    move.moveto(camera.target)
    heightControl.height=10
    sleep(5)
    #magnet command
    heightControl.height=100
    camera.colorDetector(camera.frame)
    move.moveto(camera.target)
    heightControl.height=10
    sleep(5)
    #magnet command
    heightControl.height=100
    camera.arcoDectertor(camera.frame,0)
    move.moveto(camera.target)
    heightControl.height=10
    sleep(5)
    #magnet command
    heightControl.height=100
    camera.arcoDectertor(camera.frame,1)
    move.moveto(camera.target)
    heightControl.end=True
    move.Dr.control('l')
    camera.end=True
    