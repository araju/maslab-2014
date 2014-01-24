# crazy_bot_vis.py
# a version of crazy bot that uses vision to determine distance. 
# making a new file because I don't want to deal with git right now.



import time
from mapleIf import Maple
from threading import Thread
from bump_sensor import BumpSensors
# from distance_sensor import DistanceSensors
from vision_consumer import VisionConsumer
from odometry_reading import Odometry
from motor_controller import MotorDriver
import traceback
import math

class CrazyBot:
    MOVE_FORWARD, BACK_UP, SEARCH_DIRECTION, TURN_TO_DIR = ("moveForward", "backup", "search", "turnToDir")

    def __init__(self):
        self.state = self.SEARCH_DIRECTION
        # self.state = self.BACK_UP
        self.stateStartTime = time.time();
        self.maple = Maple()
        self.driver = MotorDriver(self.maple)
        self.odo = Odometry(self.maple)
        self.bumps = BumpSensors(4,self.maple)
        self.vision = VisionConsumer(2300)
        
        self.mapleRead = True
        self.t = Thread(target = self.readMaple)
        self.t.start()
        self.vision.startServer()
        self.distances = [-1 for i in range(36)]
        self.halfFlag = 0

        time.sleep(5) # just give a bit of time to start up the vision thread


    def readMaple(self):
        while self.mapleRead:
            self.maple.periodic_task()
            time.sleep(0.01)

    def moveForwardSetup(self):
        self.stateStartTime = time.time()
        print 'move forward setup'
        return self.MOVE_FORWARD

    def moveForward(self):
        # print 'move forward bitches'
        self.driver.driveMotors(15)

        print self.vision.getWallY()

        if (self.vision.getWallY() > 270):
            print 'staph dood'
            self.driver.driveMotors(0)
            return self.backUpSetup()

        return self.MOVE_FORWARD

    def backUpSetup(self):
        self.stateStartTime = time.time()
        self.odo.distance = 0
        self.driver.driveMotors(-20)
        return self.BACK_UP

    def backUp(self):

        print self.odo.distance

        if self.odo.distance < -15:

            self.driver.driveMotors(0)
            return self.searchDirectionSetup()

        return self.BACK_UP

    def searchDirectionSetup(self):
        self.stateStartTime = time.time()
        self.halfFlag = 0
        self.distances = [-1 for i in range(36)]
        return self.SEARCH_DIRECTION

    def searchDirection(self):
        if (time.time() - self.stateStartTime < .125 and self.halfFlag == 0) or (self.halfFlag == 1 and self.odo.direction > 175):
            self.halfFlag += 1
            print 'Start Turn'
            self.driver.turnMotors(180)
            self.odo.direction = 0

        idx = int(math.floor(self.odo.direction/10) + (self.halfFlag - 1) * 18) % 36
        if (self.distances[idx] > self.vision.getWallY() or self.distances[idx] == -1): # the wall Y is inversely proportional to distance from wall
            self.distances[idx] = self.vision.getWallY()
        
        if self.odo.direction > 175 and self.halfFlag == 2:
            print 'End Turn'
            self.stateStartTime = time.time()
            self.halfFlag = 0;
            return self.turnToDirSetup()
        return self.SEARCH_DIRECTION

    def turnToDirSetup(self):
        self.stateStartTime = time.time()

        minVal = min(self.distances)
        minIdx = self.distances.index(minVal)
        self.maxDir = minIdx * 10

        self.driver.turnMotors(self.maxDir) # remember, min Y corresponds to max dist
        self.odo.direction = 0

        print 'Max distance Angle:', self.maxDir
        return self.TURN_TO_DIR

    # Assumes that self.distances is populated with a list of distances
    # The index will the heading / 10
    def turnToDir(self):

        # print self.maxDir - 5, self.odo.direction, (self.maxDir + 5) % 360

        if self.odo.direction > (self.maxDir - 5) and \
            self.odo.direction < (self.maxDir + 5) % 360:
            print 'Done Bitches'
            return self.moveForwardSetup()
            # Change state
            pass
        return self.TURN_TO_DIR

    def mainLoop(self):
        while True:
            if self.state == self.MOVE_FORWARD:
                self.state = self.moveForward()
            elif self.state == self.BACK_UP:
                self.state = self.backUp()
            elif self.state == self.SEARCH_DIRECTION:
                self.state = self.searchDirection()
            elif self.state == self.TURN_TO_DIR:
                self.state = self.turnToDir()
            time.sleep(.05)



if __name__ == '__main__':
    c = CrazyBot()
    try:
        c.mainLoop()
    except:
        traceback.print_exc()
        c.mapleRead = False
