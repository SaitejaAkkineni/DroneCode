from distance import *
import time
from Drone import Drone

def mantainAlt(height):
    Dr=Drone()
    while(height-5>distance()):
        Dr.control(inp="w")
        continue
    while(height+5>distance()):
        Dr.control(inp="s")
        continue

if __name__=="__main__":
    while True:
        time.sleep(1)
        print(distance())