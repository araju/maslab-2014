# consumes vision data and turns towards balls 
# written for the mock competition #1, but hopfulle can be used later too

import json
import socket
from threading import Thread
import traceback 


class VisionConsumer:

    def __init__(self, port):
        self.svrSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.svrSock.bind(('localhost', port))
        self.svrSock.listen(5)
        self.goalBall = [] # direction, distance of goal
        self.goalReactor = []
        self.ballMap = {"red" : [], "green" : [], "blue" : [], "reactors" : []}
        self.run = True

    
    def startServer(self):
        def runServer():
            clisock, (remhost, remport) = self.svrSock.accept()
            while self.run:
                jsonStr = clisock.recv(4096)
                print jsonStr
                self.ballMap = json.loads(jsonStr)
                
                green = self.ballMap["green"]
                red = self.ballMap["red"]
                if len(red) == 0 and len(green) == 0:
                    self.goalBall = []
                elif len(red) > len(green):
                    self.goalBall = red
                elif len(green) > len(red):
                    self.goalBall = green
                elif (red[1] < green[1]):
                    self.goalBall = red
                else:
                    self.goalBall = green

                self.goalReactor = self.ballMap["reactors"]
                

        thread = Thread(target = runServer)
        thread.start()
        print "started thread"

    def seeGreenBall(self):
        return len(self.ballMap["green"]) > 0

    def seeRedBall(self):
        return len(self.ballMap["red"]) > 0

    def seeReactor(self):
        return len(self.goalReactor) > 0

    def getWallY(self):
        if len(self.ballMap["blue"]) > 0:
            return self.ballMap["blue"][1]
        else:
            return 0


if __name__ == '__main__':
    vc = None
    try:
        vc = VisionConsumer(2300)
        vc.startServer()
    except:
        traceback.print_exc()
        if vc != None:
            vc.run = False





