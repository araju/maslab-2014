# ball_follower.py
# Visually servos to a ball or reactor.

import time
from threading import Thread
import traceback
from odometry_reading import Odometry
from mapleIf import Maple
from motor_controller import MotorDriver
from vision_consumer import VisionConsumer
from sensor_manager import SensorManager


# TODO: handle the orientation info from vision for the reactor

class BallFollower:

    NO_OBJ, TURN_TO_OBJ, GO_TO_BALL, GO_TO_REACTOR = ("noObj", "turnToObj", "goToBall", "goToReactor")
    ANGLE_THRSH = 20

    def __init__(self, maple, manager):
        self.maple = maple
        self.driver = MotorDriver(self.maple)
        # self.vision = VisionConsumer(port)
        # self.odo = Odometry(self.maple)
        self.sensorManager = manager
        
        self.state = self.NO_OBJ
        # self.mapleRead = True
        self.stateStartTime = time.time()
        # self.vision.startServer()

    # def readMaple(self):
    #     while (self.mapleRead):
    #         self.maple.periodic_task()
    #         time.sleep(0.01)

    def noObjSetup(self):
        self.stateStartTime = time.time()
        return self.NO_OBJ

    def noObj(self):
        if self.sensorManager.vision.seeGreenBall() or self.sensorManager.vision.seeRedBall():
            return self.turnToObjSetup()
        elif self.sensorManager.vision.seeReactor():
            return self.goToReactorSetup()
        else:
            return self.NO_OBJ

    def turnToObjSetup(self):
        self.stateStartTime = time.time()
        return self.TURN_TO_OBJ

    def turnToObj(self):
        goingForBall = True
        if len(self.sensorManager.vision.goalBall) == 0 and len(self.sensorManager.vision.goalReactor) == 0:
            return self.noObjSetup()# lost sight of the object
        elif len(self.sensorManager.vision.goalBall) > 0 and len(self.sensorManager.vision.goalReactor) == 0:
            goalDir = self.sensorManager.vision.goalBall[0]
            goingForBall = True
        elif len(self.sensorManager.vision.goalBall) == 0 and len(self.sensorManager.vision.goalReactor) > 0:
            goalDir = self.sensorManager.vision.goalReactor[0]
            goingForBall = False
        else:
            if self.sensorManager.vision.goalBall[1] < self.sensorManager.vision.goalReactor[1]: # ball is closer
                goalDir - self.sensorManager.vision.goalBall[0]
                goingForBall = True
            else:
                goingForBall = False
                goalDir = self.sensorManager.vision.goalReactor[0]

        if goingForBall:
            print "Turning to: ", self.sensorManager.vision.goalBall[2]
        else:
            print "Turning to: reactor"
        if abs(goalDir) < self.ANGLE_THRSH:
            self.driver.turnMotors(0)
            self.sensorManager.odo.direction = 0
            if goingForBall:
                return self.goToBallSetup()
            else:
                return self.goToReactorSetup()

        self.driver.turnMotors(-goalDir / 4.0)
        return self.TURN_TO_OBJ

    def goToBallSetup(self):
        self.stateStartTime = time.time()
        return self.GO_TO_BALL

    def goToBall(self):
        if len(self.sensorManager.vision.goalBall) == 0:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.noObjSetup()

        if abs(self.sensorManager.vision.goalBall[0]) > self.ANGLE_THRSH:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.turnToObjSetup()

        print "Going to: ", self.sensorManager.vision.goalBall[2], " , ", self.sensorManager.vision.goalBall[1]
        # self.driver.driveMotors(self.sensorManager.vision.goalBall[1])
        self.driver.driveMotors(10)
        return self.GO_TO_BALL


    def goToReactorSetup(self):
        self.stateStartTime = time.time()
        return self.GO_TO_REACTOR

    def goToReactor(self):
        if not (self.sensorManager.vision.seeReactor()):
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.noObjSetup()

        if abs(self.sensorManager.vision.goalReactor[0]) > self.ANGLE_THRSH:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.turnToObjSetup()

        self.driver.driveMotors(self.sensorManager.vision.goalReactor[1])
        return self.GO_TO_REACTOR

    def reset(self):
        self.state = self.noObjSetup()

    def mainLoop(self):
        while True:
            self.sensorManager.vision.getVisionInfo()
            self.mainIter()
            time.sleep(0.05)

    def mainIter(self):
        print self.state
        if self.state == self.NO_OBJ:
            self.state = self.noObj()
        elif self.state == self.TURN_TO_OBJ:
            self.state = self.turnToObj()
        elif self.state == self.GO_TO_BALL:
            self.state = self.goToBall()
        elif self.state == self.GO_TO_REACTOR:
            self.state = self.goToReactor()


if __name__ == '__main__':
    m = Maple()
    sense = SensorManager(2300, m)
    c = BallFollower(m,sense)
    try:
        c.mainLoop()
    except:
        traceback.print_exc()
        c.mapleRead = False





