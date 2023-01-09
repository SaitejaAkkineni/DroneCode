from distance import *
import time
import threading
from Drone import Drone


class HeightController:
    def __init__(self,height):
        self.height=height
        self.end=False
        t=threading.Thread(target=self.mantainAlt,args=self.height)
        t.start()
    def mantainAlt(self):
        Dr=Drone()
        while self.end==False:
            while(self.height-5>distance()):
                Dr.control(inp="w")
            while(self.height+5>distance()):
                Dr.control(inp="s")


if __name__=="__main__":
    while True:
        time.sleep(1)
        print(distance())