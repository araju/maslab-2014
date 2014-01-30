# consumes vision data and turns towards balls 
# written for the mock competition #1, but hopfulle can be used later too

import json
import socket
from threading import Thread
import traceback 
import subprocess
import time

class VisionConsumer:

    def __init__(self, port):
        self.svrSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.svrSock.bind(('localhost', port))
        self.svrSock.listen(5)
        self.goalBall = [] # direction, distance, color of goal
        self.goalReactor = []
        self.goalYellow = []
        self.ballMap = {"red" : [], "green" : [], "blue" : [], "reactors" : [], "yellow" : [], "wallEnds" : []}
        self.run = True

    
    def startServer(self):
        def runServer():
            clisock, (remhost, remport) = self.svrSock.accept()
            while self.run:
                jsonStr = clisock.recv(4096)
                print jsonStr
                self.ballMap = json.loads(jsonStr)
                
                # green = self.ballMap["green"]
                # green.append("green")
                # red = self.ballMap["red"]
                # red.append("red")
                # if len(red) == 1 and len(green) == 1:
                #     self.goalBall = []
                # elif len(red) > len(green):
                #     self.goalBall = red
                # elif len(green) > len(red):
                #     self.goalBall = green
                # elif (red[1] < green[1]):
                #     self.goalBall = red
                # else:
                #     self.goalBall = green

                # self.goalReactor = self.ballMap["reactors"]
                

        thread = Thread(target = runServer)
        thread.start()
        print "started thread"

    def close(self):
        self.run = False
        self.svrSock.close()

    def executeVisionProcess(self):
        printVision = False

        def printOutput(out):
            for output_line in out:
                print output_line
                # pass

        p = subprocess.Popen('java -jar vision/maslab-vision.jar',
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
        if (printVision):
            visThread = Thread(target = printOutput, args = (iter(p.stdout.readline, b''),))
            visThread.start()
        time.sleep(3)
        return p


if __name__ == '__main__':
    vc = None
    try:
        vc = VisionConsumer(2300)
        vc.startServer()
        vc.executeVisionProcess()
    except:
        traceback.print_exc()
        if vc != None:
            vc.run = False





