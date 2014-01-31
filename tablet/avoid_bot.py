# avoid_bot.py
# Handles the avoiding of obstacles

import time
import traceback

from mapleIf import Maple
from motor_controller import MotorDriver
from sensor_manager import SensorManager

class AvoidBot:

    FORWARD, BACK_UP, TURN_AROUND, DONE = ("forward", "backUp", "turnAround", "done")

    def __init__(self, maple, sensorManager):
        self.state = self.BACK_UP
        self.maple = maple
        self.sensorManager = sensorManager
        self.driver = MotorDriver(self.maple)
        self.stateStartTime = time.time
        self.turnDegrees = 180
        self.forwardMotion = False


    def backUpSetup(self):
        print "Avoid State: BACK_UP"
        self.stateStartTime = time.time()
        self.driver.driveMotors(-30)
        self.sensorManager.odo.distance = 0
        return self.BACK_UP

    def backUp(self):
        if (self.sensorManager.odo.distance < -25 or time.time() - self.stateStartTime > 5):
            return self.turnAroundSetup()
        if self.sensorManager.bumps.bumped[4]:
            return self.turnAroundSetup()
        return self.BACK_UP

    def forwardSetup(self):
        print "Avoid State: FORWARD"
        self.stateStartTime = time.time()
        self.driver.driveMotors(30)
        self.sensorManager.odo.distance = 0
        return self.FORWARD

    def forward(self):
        if self.sensorManager.odo.distance > 20 or time.time() - self.stateStartTime > 5:
            return turnAroundSetup()
        if self.sensorManager.sonars.distances[0] < 30 or self.sensorManager.sonars.distances[1] < 30:
            return turnAroundSetup()
        return self.FORWARD

    def turnAroundSetup(self):
        print "Avoid State: TURN_AROUND"
        self.stateStartTime = time.time()
        self.driver.turnMotors(self.turnDegrees)
        self.sensorManager.odo.direction = 0
        return self.TURN_AROUND

    def turnAround(self):
        if (abs(self.sensorManager.odo.direction - self.turnDegrees) < 10 or time.time() - self.stateStartTime > 5):
            return self.doneSetup()
        return self.TURN_AROUND

    def doneSetup(self):
        print "Avoid State: DONE"
        self.stateStartTime = time.time()
        self.driver.stopMotors()
        return self.DONE

    def done(self):
        return self.DONE

    def reset(self, forward, degrees):
        self.forwardMotion = forward
        self.turnDegrees = degrees
        if (forward):
            self.state = self.forwardSetup()
        else:
            self.state = self.backUpSetup()

    def mainIter(self):
        if self.state == self.BACK_UP:
            self.state = self.backUp()
        elif self.state == self.TURN_AROUND:
            self.state = self.turnAround()
        elif self.state == self.DONE:
            self.state = self.done()