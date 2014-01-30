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


class BallFollower:

    NO_OBJ, TURN_TO_OBJ, GO_TO_BALL, GO_TO_REACTOR, CLOSE_TO_BALL, GO_TO_YELLOW, AT_YELLOW, AT_REACTOR, AVOID = ("noObj", "turnToObj", "goToBall", "goToReactor", "closeToBall", "goToYellow", "atYellow", "atReactor", "avoid")
    ANGLE_THRSH = 15
    DIST_THRESH = 20 # defines when we go into close ball
    CLOSE_DIST = 50

    def __init__(self, maple, manager):
        self.maple = maple
        self.driver = MotorDriver(self.maple)
        # self.vision = VisionConsumer(port)
        # self.odo = Odometry(self.maple)
        self.sensorManager = manager
        self.gettingBall = "none"
        self.greenBallCount = 0
        self.redBallCount = 0
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
        if self.sensorManager.vision.seeObject():
            return self.turnToObjSetup()
        else:
            return self.NO_OBJ

    def turnToObjSetup(self):
        self.stateStartTime = time.time()
        return self.TURN_TO_OBJ

    def turnToObj(self):
        if time.time() - self.stateStartTime > 15:
            # something is wrong
            return self.avoidSetup()

        goingFor = 0 # 0: ball, 1: reactor, 2: yellow wall, 3: nothing
        if not self.sensorManager.vision.seeObject():
            return self.noObjSetup()# lost sight of the object

        reactorPossible = self.sensorManager.vision.seeReactor() and self.greenBallCount > 0
        yellowWallPossible = self.sensorManager.vision.seeYellowWall() and self.redBallCount > 0
        if not self.sensorManager.vision.seeBall():
            if reactorPossible and not yellowWallPossible:
                goalDir = self.sensorManager.vision.goalReactor[0]
                goingFor = 1
            elif not reactorPossible and yellowWallPossible:
                goalDir = self.sensorManager.vision.goalYellow[0]
                goingFor = 2
            elif reactorPossible and yellowWallPossible:
                if self.sensorManager.vision.goalReactor[1] < self.sensorManager.vision.goalYellow[1]:
                    goalDir = self.sensorManager.vision.goalReactor[0]
                    goingFor = 1
                else:
                    goalDir = self.sensorManager.vision.goalYellow[0]
                    goingFor = 2
            else:
                # nothing is possible
                return self.noObjSetup()
        elif not reactorPossible:
            if not yellowWallPossible:
                goalDir = self.sensorManager.vision.goalBall[0]
                goingFor = 0
            else: # see yellow and ball
                if self.sensorManager.vision.goalBall[1] < self.sensorManager.vision.goalYellow[1]:
                    goalDir = self.sensorManager.vision.goalBall[0]
                    goingFor = 0
                else:
                    goalDir = self.sensorManager.vision.goalYellow[0]
                    goingFor = 2
        elif not yellowWallPossible:
            if self.sensorManager.vision.goalBall[1] < self.sensorManager.vision.goalReactor[1]:
                goalDir = self.sensorManager.vision.goalBall[0]
                goingFor = 0
            else:
                goalDir = self.sensorManager.vision.goalReactor[0]
                goingFor = 1
        else:
            distances = [self.sensorManager.vision.goalBall[1], self.sensorManager.vision.goalReactor[1], self.sensorManager.vision.goalYellow[1]]
            minD = min(distances)
            minIdx = distances.index(minD)
            if minIdx == 0:
                goalDir = self.sensorManager.vision.goalBall[0]
                goingFor = 0
            elif minIdx == 1:
                goalDir = self.sensorManager.vision.goalReactor[0]
                goingFor = 1
            else:
                goalDir = self.sensorManager.vision.goalYellow[0]
                goingFor = 2

        # elif len(self.sensorManager.vision.goalBall) > 0 and len(self.sensorManager.vision.goalReactor) == 0:
        #     goalDir = self.sensorManager.vision.goalBall[0]
        #     goingFor = 0
        # elif len(self.sensorManager.vision.goalBall) == 0 and len(self.sensorManager.vision.goalReactor) > 0:
        #     goalDir = self.sensorManager.vision.goalReactor[0]
        #     goingForBall = False
        # else:
        #     if self.sensorManager.vision.goalBall[1] < self.sensorManager.vision.goalReactor[1] or self.greenBallCount == 0: # ball is closer
        #         goalDir = self.sensorManager.vision.goalBall[0]
        #         goingForBall = True
        #     else:
        #         goingForBall = False
        #         goalDir = self.sensorManager.vision.goalReactor[0]
        if goingFor == 0:
            print "Turning to: ", self.sensorManager.vision.goalBall[2]
        elif goingFor == 1:
            print "Turning to: reactor"
        else:
            print "Turning to: yellow"
        if abs(goalDir) < self.ANGLE_THRSH:
            self.driver.turnMotors(0)
            self.sensorManager.odo.direction = 0
            if goingFor == 0:
                return self.goToBallSetup()
            elif goingFor == 1:
                return self.goToReactorSetup()
            else:
                return self.goToYellowWallSetup()

        self.driver.turnMotors(-goalDir / 4.0)
        return self.TURN_TO_OBJ

    def goToBallSetup(self):
        self.stateStartTime = time.time()
        return self.GO_TO_BALL

    def goToBall(self):
        if time.time() - self.stateStartTime > 20:
            return self.avoidSetup()

        if len(self.sensorManager.vision.goalBall) == 0:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.noObjSetup()

        if abs(self.sensorManager.vision.goalBall[0]) > self.ANGLE_THRSH:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.turnToObjSetup()

        if self.sensorManager.vision.goalBall[1] < self.DIST_THRESH:
            self.gettingBall = self.sensorManager.vision.goalBall[2]
            return self.closeToBallSetup()

        print "Going to: ", self.sensorManager.vision.goalBall[2], " , ", self.sensorManager.vision.goalBall[1]
        # self.driver.driveMotors(self.sensorManager.vision.goalBall[1])
        self.driver.driveMotors(50)
        return self.GO_TO_BALL


    def goToReactorSetup(self):
        self.stateStartTime = time.time()
        return self.GO_TO_REACTOR

    def goToReactor(self):
        if time.time() - self.stateStartTime > 20:
            return self.avoidSetup()

        if not (self.sensorManager.vision.seeReactor()):
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.noObjSetup()

        if abs(self.sensorManager.vision.goalReactor[0]) > self.ANGLE_THRSH:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.turnToObjSetup()

        if self.sensorManager.vision.goalReactor[1] < 200:
            if self.sensorManager.bumps.bumped[0] or self.sensorManager.bumps.bumped[1] or \
                    self.sensorManager.vision.goalReactor[2] > 600 or self.sensorManager.vision.goalReactor[1] < 100:
                self.driver.driveMotors(0)
                self.sensorManager.odo.distance = 0
                return self.atReactorSetup()

        self.driver.driveMotors(self.sensorManager.vision.goalReactor[1])
        return self.GO_TO_REACTOR

    def goToYellowWallSetup(self):
        self.stateStartTime = time.time()
        return self.GO_TO_YELLOW

    def goToYellowWall(self):
        if time.time() - self.stateStartTime > 20:
            return self.avoidSetup()

        if not (self.sensorManager.vision.seeYellowWall()):
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.noObjSetup()

        if abs(self.sensorManager.vision.goalYellow[0]) > self.ANGLE_THRSH:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.turnToObjSetup()

        if self.sensorManager.vision.goalYellow[1] < 200:
            if self.sensorManager.bumps.bumped[0] or self.sensorManager.bumps.bumped[1] or \
                    self.sensorManager.vision.goalYellow[2] > 600 or \
                    self.sensorManager.vision.goalYellow[1] < 100:
                self.driver.driveMotors(0)
                self.sensorManager.odo.distance = 0
                return self.atYellowSetup()

        self.driver.driveMotors(self.sensorManager.vision.goalYellow[1])
        return self.GO_TO_YELLOW

    def atReactorSetup(self):
        self.stateStartTime = time.time()
        self.greenBallCount = 0
        self.driver.stopMotors()
        return self.AT_REACTOR

    def atReactor(self):
        if time.time() - self.stateStartTime > 10:
            return self.avoidSetup()
        return self.AT_REACTOR

    def atYellowSetup(self):
        self.stateStartTime = time.time()
        self.redBallCount = 0
        self.driver.stopMotors()
        return self.AT_YELLOW

    def atYellow(self):
        if time.time() - self.stateStartTime() > 10:
            return self.avoidSetup()
        return self.AT_YELLOW

    def closeToBallSetup(self):
        if self.gettingBall == "green":
            self.greenBallCount += 1
        if self.gettingBall == "red":
            self.redBallCount += 1
        self.stateStartTime = time.time()
        self.sensorManager.odo.distance = 0
        self.driver.driveMotors(self.CLOSE_DIST)
        return self.CLOSE_TO_BALL

    def closeToBall(self):
        if time.time() - self.stateStartTime > 10:
            return self.avoidSetup()

        if self.sensorManager.odo.distance > self.CLOSE_DIST - 2:
            self.gettingBall = "none"
            return self.noObjSetup()
        return self.CLOSE_TO_BALL

    def avoidSetup(self):
        self.stateStartTime = time.time()
        print "Hit timeout while in state: ", self.state
        self.driver.stopMotors()
        return self.AVOID

    def avoid(self):
        return self.AVOID

    def reset(self):
        self.state = self.turnToObjSetup()

    def mainLoop(self):
        while True:
            self.sensorManager.vision.getVisionInfo()
            # print self.sensorManager.vision.goalYellow
            self.mainIter()
            time.sleep(0.05)

    def mainIter(self):
        print self.state, self.greenBallCount, self.redBallCount
        if self.state == self.NO_OBJ:
            self.state = self.noObj()
        elif self.state == self.TURN_TO_OBJ:
            self.state = self.turnToObj()
        elif self.state == self.GO_TO_BALL:
            self.state = self.goToBall()
        elif self.state == self.GO_TO_REACTOR:
            self.state = self.goToReactor()
        elif self.state == self.CLOSE_TO_BALL:
            self.state = self.closeToBall()
        elif self.state == self.GO_TO_YELLOW:
            self.state = self.goToYellowWall()
        elif self.state == self.AT_YELLOW:
            self.state = self.atYellow()
        elif self.state == self.AT_REACTOR:
            self.state = self.atReactor()
        elif self.state == self.AVOID:
            self.state = self.avoid()


if __name__ == '__main__':
    m = Maple()
    sense = SensorManager(2300, m)
    c = BallFollower(m,sense)
    try:
        c.mainLoop()
    except:
        traceback.print_exc()
        c.mapleRead = False





