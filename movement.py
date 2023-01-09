from Drone import Drone

class movement():
    def __init__(self):
        self.Dr=Drone()
    def start(self):
        self.Dr.control('z')
    def moveto(self,target):
        if(abs(target[0])>50 and abs(target[1])>50):
            if(target[0]>0):
                self.Dr.control('r')
                self.Dr.control('c')
            elif(target[0]<0 and target[1]>0):
                    self.Dr.control('a')
                    self.Dr.control('c')
            elif(target[0]<0 and target[1]<0):
                    self.Dr.control('s')
                    self.Dr.control('c')
            else:
                self.Dr.control('f')
                self.Dr.control('c')
        else:
            self.Dr.control('c')