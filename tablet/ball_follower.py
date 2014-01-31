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
import subprocess


class BallFollower:

    NO_OBJ, TURN_TO_OBJ, GO_TO_BALL, GO_TO_REACTOR, CLOSE_TO_BALL, GO_TO_YELLOW, AT_YELLOW, AT_REACTOR, AVOID = ("noObj", "turnToObj", "goToBall", "goToReactor", "closeToBall", "goToYellow", "atYellow", "atReactor", "avoid")
    ANGLE_THRSH = 15
    DIST_THRESH = 20 # defines when we go into close ball
    CLOSE_DIST = 20

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
        self.bumpsHit = False

        self.avoidForward = False
        self.avoidDegrees = 180
        # self.vision.startServer()

    # def readMaple(self):
    #     while (self.mapleRead):
    #         self.maple.periodic_task()
    #         time.sleep(0.01)

    def noObjSetup(self):
        print "Ball State: NO_OBJ", self.greenBallCount, self.redBallCount
        self.stateStartTime = time.time()
        self.driver.driveMotors(0)
        return self.NO_OBJ

    def noObj(self):
        if self.sensorManager.vision.seeObject():
            return self.turnToObjSetup()
        else:
            return self.NO_OBJ

    def turnToObjSetup(self):
        print "Ball State: TURN_TO_OBJ", self.greenBallCount, self.redBallCount
        self.driver.driveMotors(0)
        time.sleep(1)
        self.stateStartTime = time.time()
        self.bumpsHit = False
        return self.TURN_TO_OBJ

    def turnToObj(self):
        if time.time() - self.stateStartTime > 20:
            # something is wrong
            bumpSensors = self.sensorManager.bumps.bumped
            if bumpSensors[0] or bumpSensors[1] or bumpSensors[2]:
                return self.avoidSetup(False, 0)
            elif bumpSensors[3] or bumpSensors[4] or bumpSensors[5]:
                return self.avoidSetup(True, 0) 
            else:
                return self.avoidSetup(False, 90)

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

        if goingFor == 0:
            print "Turning to: ", self.sensorManager.vision.goalBall[2], goalDir
        elif goingFor == 1:
            print "Turning to: reactor", goalDir
        else:
            print "Turning to: yellow", goalDir
        if abs(goalDir) < self.ANGLE_THRSH:
            self.driver.turnMotors(0)
            self.sensorManager.odo.direction = 0
            if goingFor == 0:
                return self.goToBallSetup()
            elif goingFor == 1:
                return self.goToReactorSetup()
            else:
                return self.goToYellowWallSetup()

        bumpSensors = self.sensorManager.bumps.bumped
        if not self.bumpsHit and (bumpSensors[0] or bumpSensors[1] or bumpSensors[2] or bumpSensors[3] or bumpSensors[4] or bumpSensors[5]):
            self.stateStartTime = time.time() - 18.0
            self.bumpsHit = True

        self.driver.turnMotors(-goalDir / 6.2)
        return self.TURN_TO_OBJ

    def goToBallSetup(self):
        print "Ball State: GO_TO_BALL", self.greenBallCount, self.redBallCount
        print "Going to: ", self.sensorManager.vision.goalBall[2], " , ", self.sensorManager.vision.goalBall[1]
        if self.sensorManager.vision.goalBall[2] == "green":
            self.greenBallCount += 1
        else:
            self.redBallCount += 1
        self.stateStartTime = time.time()
        self.bumpsHit = False
        return self.GO_TO_BALL

    def goToBall(self):
        if time.time() - self.stateStartTime > 20:
            if (self.sensorManager.vision.seeBall()):
                if self.sensorManager.vision.goalBall[0] > 0:
                    return self.avoidSetup(False, -90)
                else:
                    return self.avoidSetup(False, 90)
            else:
                return self.avoidSetup(False, 90)

        if len(self.sensorManager.vision.goalBall) == 0:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.noObjSetup()

        if abs(self.sensorManager.vision.goalBall[0]) > self.ANGLE_THRSH:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.turnToObjSetup()

        if not self.bumpsHit and (self.sensorManager.bumps.bumped[0] or self.sensorManager.bumps.bumped[1]):
            if self.sensorManager.vision.goalBall[1] > 30:
                if self.sensorManager.vision.goalBall[0] > 0:
                    return self.avoidSetup(False, -45)
                else:
                    return self.avoidSetup(False, 45)
            self.bumpsHit = True
            self.stateStartTime = time.time() - 18

        if self.sensorManager.vision.goalBall[1] < self.DIST_THRESH:
            self.gettingBall = self.sensorManager.vision.goalBall[2]
            return self.closeToBallSetup()

        # self.driver.driveMotors(self.sensorManager.vision.goalBall[1])
        self.driver.driveMotors(20)
        return self.GO_TO_BALL


    def goToReactorSetup(self):
        print "Ball State: GO_TO_REACTOR", self.greenBallCount, self.redBallCount
        self.driver.driveMotors(0)
        self.stateStartTime = time.time()
        self.bumpsHit = False
        return self.GO_TO_REACTOR

    def goToReactor(self):
        if time.time() - self.stateStartTime > 20:
            if (self.sensorManager.vision.seeReactor()):
                if self.sensorManager.vision.goalReactor[0] > 0:
                    return self.avoidSetup(False, -45)
                else:
                    return self.avoidSetup(False, 45)
            else:
                return self.avoidSetup(False, 90)

        if not (self.sensorManager.vision.seeReactor()):
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.noObjSetup()

        if abs(self.sensorManager.vision.goalReactor[0]) > self.ANGLE_THRSH:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.turnToObjSetup()


        if self.sensorManager.vision.goalReactor[1] < 100:
            if self.sensorManager.bumps.bumped[0] or self.sensorManager.bumps.bumped[1] or \
                    self.sensorManager.vision.goalReactor[2] > 300 or self.sensorManager.vision.goalReactor[1] < 50:
                self.driver.driveMotors(0)
                self.sensorManager.odo.distance = 0
                return self.atReactorSetup()

        if not self.bumpsHit and (self.sensorManager.bumps.bumped[0] or self.sensorManager.bumps.bumped[1]):
            if self.sensorManager.vision.goalReactor[1] > 140:
                if self.sensorManager.vision.goalReactor[0] > 0:
                    return self.avoidSetup(False, -45)
                else:
                    return self.avoidSetup(False, 45)
            self.bumpsHit = True
            self.stateStartTime = time.time() - 18

        self.driver.driveMotors(self.sensorManager.vision.goalReactor[1])
        return self.GO_TO_REACTOR

    def goToYellowWallSetup(self):
        print "Ball State: GO_TO_YELLOW", self.greenBallCount, self.redBallCount
        self.stateStartTime = time.time()
        self.bumpsHit = False
        return self.GO_TO_YELLOW

    def goToYellowWall(self):
        if time.time() - self.stateStartTime > 20:
            if (self.sensorManager.vision.seeYellowWall()):
                if self.sensorManager.vision.goalYellow[0] > 0:
                    return self.avoidSetup(False, -45)
                else:
                    return self.avoidSetup(False, 45)
            else:
                return self.avoidSetup(False, 90)

        if not (self.sensorManager.vision.seeYellowWall()):
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.noObjSetup()

        if abs(self.sensorManager.vision.goalYellow[0]) > self.ANGLE_THRSH * 1.5:
            self.driver.driveMotors(0)
            self.sensorManager.odo.distance = 0
            return self.turnToObjSetup()

        

        if self.sensorManager.vision.goalYellow[1] < 100:
            if self.sensorManager.bumps.bumped[0] or self.sensorManager.bumps.bumped[1] or \
                    self.sensorManager.vision.goalYellow[2] > 300 or \
                    self.sensorManager.vision.goalYellow[1] < 50:
                self.driver.driveMotors(0)
                self.sensorManager.odo.distance = 0
                return self.atYellowSetup()

        if not self.bumpsHit and (self.sensorManager.bumps.bumped[0] or self.sensorManager.bumps.bumped[1]):
            if self.sensorManager.vision.goalYellow[1] > 140:
                if self.sensorManager.vision.goalYellow[0] > 0:
                    return self.avoidSetup(False, -45)
                else:
                    return self.avoidSetup(False, 45)
            self.bumpsHit = True
            self.stateStartTime = time.time() - 18

        self.driver.driveMotors(self.sensorManager.vision.goalYellow[1])
        return self.GO_TO_YELLOW

    def atReactorSetup(self):
        print "Ball State: AT_REACTOR", self.greenBallCount, self.redBallCount
        self.stateStartTime = time.time()
        self.greenBallCount = 0
        self.driver.stopMotors()
        return self.AT_REACTOR

    def atReactor(self):
        # if time.time() - self.stateStartTime > 10:
        #     return self.avoidSetup()
        return self.AT_REACTOR

    def atYellowSetup(self):
        print "Ball State: AT_YELLOW", self.greenBallCount, self.redBallCount
        self.stateStartTime = time.time()
        self.redBallCount = 0
        self.driver.stopMotors()
        return self.AT_YELLOW

    def atYellow(self):
        # if time.time() - self.stateStartTime() > 10:
        #     return self.avoidSetup()
        return self.AT_YELLOW

    def closeToBallSetup(self):
        print "Ball State: CLOSE_TO_BALL", self.greenBallCount, self.redBallCount
        # if self.gettingBall == "green":
        #     self.greenBallCount += 1
        # if self.gettingBall == "red":
        #     self.redBallCount += 1
        self.stateStartTime = time.time()
        self.sensorManager.odo.distance = 0
        self.driver.driveMotors(self.CLOSE_DIST)
        return self.CLOSE_TO_BALL

    def closeToBall(self):
        if time.time() - self.stateStartTime > 7:
            return self.avoidSetup(False, 180)

        if self.sensorManager.odo.distance > self.CLOSE_DIST - 2:
            self.gettingBall = "none"
            return self.noObjSetup()
        return self.CLOSE_TO_BALL

    def avoidSetup(self, forward, degrees):
        self.avoidForward = forward
        self.avoidDegrees = degrees
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

    def executeVisionProcess(self):
        printVision = True

        def printOutput(out):
            print "in print"
            for output_line in out:
                print output_line
                #pass
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


if __name__ == '__main__':
    m = Maple()
    sense = SensorManager(2300, m)
    c = BallFollower(m,sense)
    try:
        c.executeVisionProcess()
        c.mainLoop()
    except:
        traceback.print_exc()
    finally:
        c.mapleRead = False
        sense.close()





