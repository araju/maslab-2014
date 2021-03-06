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
import subprocess

class CrazyBot:
    MOVE_FORWARD, BACK_UP, SEARCH_DIRECTION, TURN_TO_DIR, UNSTUCK_TURN = ("moveForward", "backup", "searchDirection", "turnToDir", 'unstuckTurn')

    def __init__(self, maple, manager):
        self.state = self.MOVE_FORWARD
        #self.state = self.SEARCH_DIRECTION
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

        # for seeing when we are stuck in turns



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
        self.driver.driveMotors(20)

        # print "Sonar Distances: ", self.sensorManager.sonars.distances[0]

        if (self.sensorManager.bumps.bumped[0] or self.sensorManager.bumps.bumped[1]):
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
        if self.sensorManager.odo.distance < -30:
            self.driver.driveMotors(0)
            return self.searchDirectionSetup()

        return self.BACK_UP

    def searchDirectionSetup(self):
        self.stateStartTime = time.time()
        self.halfFlag = 1
        self.distances = [-1 for i in range(36)]
        self.driver.turnMotors(180)
        self.stuckCounter = 0

        print "State: SEARCH_DIRECTION"
        return self.SEARCH_DIRECTION

    def searchDirection(self):
        if (self.halfFlag == 1 and self.sensorManager.odo.direction > 175):
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

        if abs(self.sensorManager.odo.angularRate) < 5:
            self.stuckCounter += 1

        if self.stuckCounter > 100:
            print 'HALP I"M STUCKZ!!!'
            return self.unstuckTurnSetup()
        return self.SEARCH_DIRECTION

    def unstuckTurnSetup(self):
        self.stateStartTime = time.time()
        self.driver.turnMotors(-15)
        return self.UNSTUCK_TURN

    def unstuckTurn(self):
        if self.sensorManager.odo.direction < 350 and self.sensorManager.odo.direction > 5:
            return self.backUpSetup()

        return self.UNSTUCK_TURN


    def turnToDirSetup(self):
        self.stateStartTime = time.time()

        print "Distances: ", self.distances
        maxVal = max(self.distances)
        maxIdx = self.distances.index(maxVal)
        self.maxDir = maxIdx * 10

        if random.random() < .333:
            self.maxDir = random.randint(0, 359)

        self.driver.turnMotors(self.maxDir)

        self.sensorManager.odo.direction = 0

        print 'Max distance Angle:', self.maxDir
        print "State: TURN_TO_DIR"
        self.stuckCounter = 0
        return self.TURN_TO_DIR

    # Assumes that self.distances is populated with a list of distances
    # The index will the heading / 10
    def turnToDir(self):
        if self.sensorManager.odo.direction > (self.maxDir - 5) and \
            self.sensorManager.odo.direction < (self.maxDir + 5) % 360:
            print 'Done Bitches'
            return self.moveForwardSetup()

        if abs(self.sensorManager.odo.angularRate) < 5:
            self.stuckCounter += 1

        if self.stuckCounter > 100:
            print 'HALP I"M STUCKZ!!!'
            return self.unstuckTurnSetup()
        return self.TURN_TO_DIR

    def reset(self):
        self.state = self.moveForwardSetup()

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
            if time.time() - self.stateStartTime > 4:
                print "timed out"
                self.state = self.searchDirectionSetup()
        elif self.state == self.SEARCH_DIRECTION:
            self.state = self.searchDirection()
            if time.time() - self.stateStartTime > 7:
                print "timed out"
                self.state = self.turnToDirSetup()
        elif self.state == self.TURN_TO_DIR:
            self.state = self.turnToDir()
            if time.time() - self.stateStartTime > 7:
                print "timed out"
                self.state = self.moveForwardSetup()
        elif self.state == self.UNSTUCK_TURN:
            self.state = self.unstuckTurn()
            if time.time() - self.stateStartTime > 2:
                print "timed out"
                self.state = self.backUpSetup()

    def waitForStart(self):
        def handleOutput(out):
            for output_line in out:
                # if output_line == "GAME-STARTED-BITCHES":
                #     self.gameStarted = True
                #     break
                print output_line
                self.gameStarted = True
                break
        
        self.gameStarted = False
        p = subprocess.Popen('C:/Program Files (x86)/Java/bin/java.exe -jar BotClient/Java/botclient.jar',
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
        botClientThread = Thread(target = handleOutput, args = (iter(p.stdout.readline, b''),))
        botClientThread.start()

        while not self.gameStarted:
            time.sleep(0.1)

        try:
            p.kill()
        except:
            traceback.print_exc()
            
        time.sleep(2)

if __name__ == '__main__':
    m = Maple()
    sense = SensorManager(2300, m)
    c = CrazyBot(m, sense)
    try:
        #c.waitForStart()
        c.mainLoop()
    except:
        traceback.print_exc()
        c.mapleRead = False
