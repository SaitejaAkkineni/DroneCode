import gpiozero as pig
import time
from Drone import Drone

reading=True
sensor=pig.DistanceSensor(echo=24,trigger=23)

def distance():
    while reading:
        distance=sensor.value*100
        print(distance)
    return distance

def mantainAlt(height):
    while(height-10>distance()):
        Drone.control('w')
        continue
    while(height+10>distance()):
        Drone.control('s')
        continue

if __name__=="__main__":
    while True:
        time.sleep(1)
        print(distance())