# score_bot.py
# Handles the lining up to the wall and the dumping ball process

import time
import traceback
import subprocess
from threading import Thread

from mapleIf import Maple
from motor_controller import MotorDriver
from sensor_manager import SensorManager



class ScoreBot():
    
    LINING, MOVE_FORWARD, DUMP_RED, DUMP_GREEN, TURN_AWAY, BACK_UP, IDLE = ("lining", "moveForward", "dumpRed", "dumpGreen", "turnAway", "backUp", "idle")

    def __init__(self, maple, sensorManager):
        self.maple = maple
        self.sensorManager = sensorManager
        self.driver = MotorDriver(self.maple)
        self.state = self.IDLE
        self.atReactor = True #whether we are at a reactor or a yellow wall
    

    def liningSetup(self):
        self.stateStartTime = time.time()
        self.driveMotors(0)
        return self.LINING

    def lining(self):
        if time.time() - self.stateStartTime > 10:
            print "Timed out of lining"
            return self.moveForwardSetup() # just moveForward and hope for the best
        wallEnds = self.sensorManager.vision.ballMap["wallEnds"]
        if self.sensorManager.bumps.bumped[0] and self.sensorManager.bumps.bumped[1]:
            self.driver.stopMotors()
            return self.moveForwardSetup()
        elif len(wallEnds) > 0 and abs(wallEnds[0] - wallEnds[1]) < 20:
            print "wall ends lined up in image"
            self.driver.stopMotors()
            return self.moveForwardSetup()
        elif self.sensorManager.bumps.bumped[0]:
            self.driver.driveMotorPWM(0,100)
            # self.driver.turnMotors(5)
            return self.LINING
        elif self.sensorManager.bumps.bumped[1]:
            self.driver.driveMotorPWM(100,0)
            # self.driver.turnMotors(-5)
            return self.LINING
        if len(wallEnds) > 0:
            elif wallEnds[0] - wallEnds[1] < 0:
                self.driver.driveMotorPWM(100,0)
                return self.LINING
            else:
                self.driver.driveMotorPWM(0,100)
                return self.LINING
        # if self.sensorManager.bumps.bumped[0]:
        #     # self.driver.driveMotorPWM(0,200)
        #     self.driver.turnMotors(5)
        #     return self.LINING
        # if self.sensorManager.bumps.bumped[1]:
        #     # self.driver.driveMotorPWM(200,0)
        #     self.driver.turnMotors(-5)
        #     return self.LINING
        print "just driving forward in LINING"
        self.driver.driveMotors(15)
        return self.LINING

    def moveForwardSetup(self):
        print "Score State: MOVE_FORWARD"
        self.stateStartTime = time.time()
        self.driver.driveMotors(15)
        self.sensorManager.odo.distance = 0
        return self.MOVE_FORWARD

    def moveForward(self):
        if (self.sensorManager.odo.distance > 25 or time.time() - self.stateStartTime > 1):
            self.driver.stopMotors()
            if (self.atReactor):
                return self.dumpGreenSetup()
            else:
                return self.dumpRedSetup()
        return self.MOVE_FORWARD

    def dumpRedSetup(self):
        print "Score State: DUMP_RED"
        self.stateStartTime = time.time()
        self.driver.dumpRed()
        return self.DUMP_RED

    def dumpRed(self):
        if (time.time() - self.stateStartTime > 1):
            return self.backUpSetup()
        return self.DUMP_RED

    def dumpGreenSetup(self):
        print "Score State: DUMP_GREEN"
        self.stateStartTime = time.time()
        self.driver.dumpGreen()
        return self.DUMP_GREEN

    def dumpGreen(self):
        if (time.time() - self.stateStartTime > 1):
            return self.backUpSetup()
        return self.DUMP_GREEN

    def idleSetup(self):
        self.stateStartTime = time.time()
        return self.IDLE

    def backUpSetup(self):
        print "Score State: BACK_UP"
        self.stateStartTime = time.time()
        self.driver.driveMotors(-30)
        self.sensorManager.odo.distance = 0
        return self.BACK_UP

    def backUp(self):
        if (self.sensorManager.odo.distance < -25 or time.time() - self.stateStartTime > 3):
            return self.turnAwaySetup()
        return self.BACK_UP

    def turnAwaySetup(self):
        print "Score State: TURN_AWAY"
        self.stateStartTime = time.time()
        self.driver.turnMotors(180)
        self.sensorManager.odo.direction = 0
        return self.TURN_AWAY

    def turnAway(self):
        if (self.sensorManager.odo.direction > 170 or time.time() - self.stateStartTime > 5):
            return self.idleSetup()
        return self.TURN_AWAY

    def idle(self):
        return self.IDLE

    def reset(self):
        self.state = self.liningSetup()

    def executeVisionProcess(self):
        def printOutput(out):
            for output_line in out:
                # print output_line
                pass

        try:
            p = subprocess.Popen('java -jar vision/maslab-vision.jar',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        except: # maybe we are on the tablet
            p = subprocess.Popen('C:/Program Files (x86)/Java/jdk1.7.0_45/bin/java.exe -jar vision/maslab-vision.jar',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)

        visThread = Thread(target = printOutput, args = (iter(p.stdout.readline, b''),))
        visThread.start()
        time.sleep(3)
        
        return p

    def mainIter(self):
        if self.state == self.IDLE:
            self.state = self.idle()
        elif self.state == self.DUMP_GREEN:
            self.state = self.dumpGreen()
        elif self.state == self.DUMP_RED:
            self.state = self.dumpRed()
        elif self.state == self.LINING:
            self.state = self.lining()
        elif self.state == self.MOVE_FORWARD:
            self.state = self.moveForward()
        elif self.state == self.TURN_AWAY:
            self.state = self.turnAway()
        elif self.state == self.BACK_UP:
            self.state = self.backUp()

    def mainLoop(self):
        while True:
            self.mainIter()
            time.sleep(0.05)


if __name__ == '__main__':
    m = Maple()
    sense = SensorManager(2300, maple)
    s = ScoreBot(m,sense)
    try:
        s.executeVisionProcess()
        s.mainLoop()
    except:
        traceback.print_exc()


