# avoid_bot.py
# Handles the avoiding of obstacles

import time
import traceback

from mapleIf import Maple
from motor_controller import MotorDriver
from sensor_manager import SensorManager

class AvoidBot:

    BACK_UP, TURN_AROUND, DONE = ("backUp", "turnAround", "done")

    def __init__(self, maple, sensorManager):
        self.state = self.DONE
        self.maple = maple
        self.sensorManager = sensorManager
        self.driver = MotorDriver(self.maple)
        self.stateStartTime = time.time
        self.turnDegrees = 180


    def backUpSetup(self):
        self.stateStartTime = time.time()
        self.driver.driveMotors(-30)
        self.sensorManager.odo.distance = 0
        return self.BACK_UP

    def backUp(self):
        if (self.sensorManager.odo.distance < -25 or time.time() - self.stateStartTime > 5):
            return self.turnAroundSetup()
        return self.BACK_UP

    def turnAroundSetup(self):
        self.stateStartTime = time.time()
        self.driver.turnMotors(self.turnDegrees)
        self.sensorManager.odo.direction = 0
        return self.TURN_AROUND

    def turnAround(self):
        if (abs(self.sensorManager.odo.direction - self.turnDegrees) < 10 or time.time() - self.stateStartTime > 5):
            return self.doneSetup()
        return self.TURN_AROUND

    def doneSetup(self):
        self.stateStartTime = time.time()
        self.driver.stopMotors()
        return self.DONE

    def done(self):
        return self.DONE

    def reset(self, degrees):
        self.turnDegrees = degrees
        self.state = self.backUpSetup()

    def mainIter(self):
        if self.state == self.BACK_UP:
            self.state = self.backUp()
        elif self.state == self.TURN_AROUND:
            self.state = self.turnAround()
        elif self.state == self.DONE:
            self.state = self.done()