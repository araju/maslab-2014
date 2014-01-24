# crazy_bot.py
# This shit is crazy. Bot goes in random directions and turns when it hits a wall

import time
from mapleIf import Maple
from threading import Thread
from bump_sensor import BumpSensors
from distance_sensor import DistanceSensors
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
        self.sonars = DistanceSensors(4,self.maple)
        
        self.mapleRead = True
        self.t = Thread(target = self.readMaple)
        self.t.start()
        self.distances = [-1 for i in range(36)]
        self.halfFlag = 0


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

        print self.sonars.distances[0]

        if (self.sonars.distances[0] < 20):
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
            
        print self.sonars.distances

        idx = int(math.floor(self.odo.direction/10) + (self.halfFlag - 1) * 18) % 36
        if (self.distances[idx] < self.sonars.distances[0]):
            self.distances[idx] = self.sonars.distances[0]
        
        if self.odo.direction > 175 and self.halfFlag == 2:
            print 'End Turn'
            self.stateStartTime = time.time()
            self.halfFlag = 0;
            return self.turnToDirSetup()
        return self.SEARCH_DIRECTION

    def turnToDirSetup(self):
        self.stateStartTime = time.time()

        maxVal = max(self.distances)
        maxIdx = self.distances.index(maxVal)
        self.maxDir = maxIdx * 10

        self.driver.turnMotors(self.maxDir)
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
                if time.time() - self.stateStartTime > 15:
                    self.state = self.backUpSetup()
            elif self.state == self.BACK_UP:
                self.state = self.backUp()
                if time.time() - self.stateStartTime > 15:
                    self.state = self.searchDirectionSetup()
            elif self.state == self.SEARCH_DIRECTION:
                self.state = self.searchDirection()
                if time.time() - self.stateStartTime > 15:
                    self.state = self.turnToDirSetup()
            elif self.state == self.TURN_TO_DIR:
                self.state = self.turnToDir()
                if time.time() - self.stateStartTime > 15:
                    self.state = self.moveForwardSetup()
            time.sleep(.05)



if __name__ == '__main__':
    c = CrazyBot()
    try:
        c.mainLoop()
    except:
        traceback.print_exc()
        c.mapleRead = False
