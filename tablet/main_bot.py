# main_bot.py
# switches between the crazy bot and the ball follower. hell ya

import time
import traceback
import subprocess
from threading import Thread
import sys
from crazy_bot import CrazyBot
from ball_follower import BallFollower
from score_bot import ScoreBot
from avoid_bot import AvoidBot
from sensor_manager import SensorManager
from mapleIf import Maple
from motor_controller import MotorDriver

class MainBot:
    
    SEARCH, BALL_FOLLOW, SCORE, AVOID = ("search", "ball_follow", "score", "avoid")

    def __init__(self):
        self.maple = Maple()
        self.sensorManager = SensorManager(2300, self.maple)
        self.searchBot = CrazyBot(self.maple, self.sensorManager)
        self.ballFollower = BallFollower(self.maple, self.sensorManager)
        self.scoreBot = ScoreBot(self.maple, self.sensorManager)
        self.avoidBot = AvoidBot(self.maple, self.sensorManager)
        self.state = self.SEARCH
        self.stateStartTime = time.time()
        self.visionProcess = self.executeVisionProcess()
        self.driver = MotorDriver(self.maple)
        self.gameStarted = True
        self.prevState = self.SEARCH

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

    def searchSetup(self):
        self.stateStartTime = time.time()
        self.searchBot.reset()
        print "Main State: SEARCH"
        return self.SEARCH

    def search(self):
        if self.sensorManager.vision.seeObject():
            if self.sensorManager.vision.seeBall() or (self.sensorManager.vision.seeReactor() and self.ballFollower.greenBallCount > 0) or (self.sensorManager.vision.seeYellowWall() and self.ballFollower.redBallCount > 0):
                return self.ballFollowSetup()
        self.searchBot.mainIter()
        return self.SEARCH

    def ballFollowSetup(self):
        self.stateStartTime = time.time()
        self.driver.stopMotors()
        self.ballFollower.reset()
        print "Main State: BALL_FOLLOW"
        return self.BALL_FOLLOW

    def ballFollow(self):
        if self.ballFollower.state == self.ballFollower.AVOID:
            self.driver.stopMotors()
            return self.avoidSetup(self.ballFollower.avoidForward, self.ballFollower.avoidDegrees)
        if self.ballFollower.state == self.ballFollower.AT_REACTOR:
            self.driver.stopMotors()
            return self.scoreSetup(True)
        if self.ballFollower.state == self.ballFollower.AT_YELLOW:
            self.driver.stopMotors()
            return self.scoreSetup(False)
        if not self.sensorManager.vision.seeObject() or \
                self.ballFollower.state == self.ballFollower.NO_OBJ:
            return self.searchSetup()
        # elif (not self.sensorManager.vision.seeBall()):
        #     if self.sensorManager.vision.seeReactor() and (self.ballFollower.greenBallCount == 0):
        #         # don't see any balls and don't have any balls
        #         return self.searchSetup()
        self.ballFollower.mainIter()
        return self.BALL_FOLLOW

    def scoreSetup(self, atReactor):
        self.stateStartTime = time.time()
        self.scoreBot.reset()
        self.scoreBot.atReactor = atReactor
        print "Main State: SCORE"
        return self.SCORE

    def score(self):
        if (self.scoreBot.state == self.scoreBot.IDLE):
            # done scoring
            return self.searchSetup()
        elif (self.scoreBot.state == self.scoreBot.RETRY_DONE):
            if self.scoreBot.atReactor:
                self.ballFollower.greenBallCount += 1
            else:
                self.ballFollower.redBallCount += 1
            return self.ballFollowSetup() # try to line up again
        self.scoreBot.mainIter()
        return self.SCORE

    def avoidSetup(self, forward, degrees):
        self.prevState = self.state
        print "Prev State: ", self.prevState
        self.stateStartTime = time.time()
        self.avoidBot.reset(forward, degrees)
        print "Main State: AVOID"
        return self.AVOID

    def avoid(self):
        if (self.avoidBot.state == self.avoidBot.DONE):
            self.driver.stopMotors()
            print "Avoid State Over in Main: ", self.prevState
            if self.prevState == self.SEARCH:
                return self.searchSetup()
            elif self.prevState == self.BALL_FOLLOW:
                return self.ballFollowSetup()
            elif self.prevState == self.SCORE:
                return self.scoreSetup()
            else:
                return self.searchSetup()
        self.avoidBot.mainIter()
        return self.AVOID


    def mainIter(self):
        # print self.state
        if self.state == self.SEARCH:
            self.state = self.search()
        elif self.state == self.BALL_FOLLOW:
            self.state = self.ballFollow()
        elif self.state == self.SCORE:
            self.state = self.score()
        elif self.state == self.AVOID:
            self.state = self.avoid()

    def mainLoop(self):
        while True:
            self.sensorManager.vision.getVisionInfo()
            # if len(self.sensorManager.vision.goalBall) > 0:
            #     print self.sensorManager.vision.goalBall[2]
            self.mainIter()
            time.sleep(0.01)

    
    def waitForStart(self):
        def handleOutput(out):
            for output_line in out:
                if output_line.startswith("GAME-STARTED-BITCHES"):
                    self.gameStarted = True
                    break
        
        self.gameStarted = False
        p = subprocess.Popen(['java','-jar','BotClient/Java/botclient.jar'],
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
        


    def closeMaple(self):
        self.sensorManager.close()


if __name__ == '__main__':
    m = MainBot()
    try:
        # m.waitForStart()
        m.mainLoop()
    except:
        traceback.print_exc()
        m.visionProcess.kill()
        m.closeMaple()


