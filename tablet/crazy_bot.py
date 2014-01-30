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
from music import playMusic
import random
from sensor_manager import SensorManager

class CrazyBot:
    MOVE_FORWARD, BACK_UP, SEARCH_DIRECTION, TURN_TO_DIR = ("moveForward", "backup", "searchDirection", "turnToDir")

    def __init__(self, maple, manager):
        self.state = self.SEARCH_DIRECTION
        # self.state = self.BACK_UP
        self.stateStartTime = time.time();
        self.maple = maple
        self.sensorManager = manager
        self.driver = MotorDriver(self.maple)
        # self.odo = Odometry(self.maple)
        # self.bumps = BumpSensors(4,self.maple)
        # self.sonars = DistanceSensors(4,self.maple)
        
        # self.mapleRead = True
        # self.t = Thread(target = self.readMaple)
        # self.t.start()
        self.distances = [-1 for i in range(36)]
        self.halfFlag = 0
        # playMusic.play()


    # def readMaple(self):
    #     while self.mapleRead:
    #         self.maple.periodic_task()
    #         time.sleep(0.01)

    def moveForwardSetup(self):
        self.stateStartTime = time.time()
        print "State: MOVE_FORWARD"
        return self.MOVE_FORWARD

    def moveForward(self):
        # print 'move forward bitches'
        self.driver.driveMotors(15)

        # print "Sonar Distances: ", self.sensorManager.sonars.distances[0]

        if (self.sensorManager.sonars.distances[0] < 20 or self.sensorManager.sonars.distances[1] < 20 or
                self.sensorManager.bumps.bumped[0] or self.sensorManager.bumps.bumped[1]):
            print 'staph dood'
            self.driver.driveMotors(0)
            return self.backUpSetup()

        return self.MOVE_FORWARD

    def backUpSetup(self):
        self.stateStartTime = time.time()
        self.sensorManager.odo.distance = 0
        self.driver.driveMotors(-35)
        print "State: BACK_UP"
        return self.BACK_UP

    def backUp(self):

        # print "Odo dist: ", self.sensorManager.odo.distance

        if self.sensorManager.odo.distance < -30 or self.sensorManager.bumps.bumped[4]:
            self.driver.driveMotors(0)
            return self.searchDirectionSetup()

        return self.BACK_UP

    def searchDirectionSetup(self):
        self.stateStartTime = time.time()
        self.halfFlag = 0
        self.distances = [-1 for i in range(36)]
        print "State: SEARCH_DIRECTION"
        return self.SEARCH_DIRECTION

    def searchDirection(self):
        if (time.time() - self.stateStartTime < .125 and self.halfFlag == 0) or (self.halfFlag == 1 and self.sensorManager.odo.direction > 175):
            self.halfFlag += 1
            print 'Start Turn'
            self.driver.turnMotors(180)
            self.sensorManager.odo.direction = 0
            
        # print self.sensorManager.sonars.distances

        idx = int(math.floor(self.sensorManager.odo.direction/10) + (self.halfFlag - 1) * 18) % 36
        currDist = (self.sensorManager.sonars.distances[0] + self.sensorManager.sonars.distances[1]) / 2.0
        if (self.distances[idx] < currDist):
            self.distances[idx] = currDist
        
        if self.sensorManager.odo.direction > 175 and self.halfFlag == 2:
            print 'End Turn'
            self.stateStartTime = time.time()
            self.halfFlag = 0;
            return self.turnToDirSetup()
        return self.SEARCH_DIRECTION

    def turnToDirSetup(self):
        self.stateStartTime = time.time()

        print "Distances: ", self.distances
        maxVal = max(self.distances)
        maxIdx = self.distances.index(maxVal)
        self.maxDir = maxIdx * 10

        # self.maxDir = random.randint(0, 359)
        # print self.maxDir

        self.driver.turnMotors(self.maxDir)

        self.sensorManager.odo.direction = 0

        print 'Max distance Angle:', self.maxDir
        print "State: TURN_TO_DIR"
        return self.TURN_TO_DIR

    # Assumes that self.distances is populated with a list of distances
    # The index will the heading / 10
    def turnToDir(self):
        if self.sensorManager.odo.direction > (self.maxDir - 5) and \
            self.sensorManager.odo.direction < (self.maxDir + 5) % 360:
            print 'Done Bitches'
            return self.moveForwardSetup()
        return self.TURN_TO_DIR

    def reset(self):
        self.state = self.searchDirectionSetup()

    def mainLoop(self):
        while True:
            self.mainIter()
            # print "Orientation: ", self.sensorManager.odo.direction
            # print "LRIR: ", self.sensorManager.sonars.distances[0]
            time.sleep(.05)

    def mainIter(self):
        # print "State: ", self.state
        if self.state == self.MOVE_FORWARD:
            self.state = self.moveForward()
            if time.time() - self.stateStartTime > 15:
                print "timed out"
                self.state = self.backUpSetup()
        elif self.state == self.BACK_UP:
            self.state = self.backUp()
            if time.time() - self.stateStartTime > 15:
                print "timed out"
                self.state = self.searchDirectionSetup()
        elif self.state == self.SEARCH_DIRECTION:
            self.state = self.searchDirection()
            if time.time() - self.stateStartTime > 15:
                print "timed out"
                self.state = self.turnToDirSetup()
        elif self.state == self.TURN_TO_DIR:
            self.state = self.turnToDir()
            if time.time() - self.stateStartTime > 15:
                print "timed out"
                self.state = self.moveForwardSetup()



if __name__ == '__main__':
    m = Maple()
    sense = SensorManager(2300, m)
    c = CrazyBot(m, sense)
    try:
        c.mainLoop()
    except:
        traceback.print_exc()
        c.mapleRead = False
