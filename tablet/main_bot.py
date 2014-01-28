# main_bot.py
# switches between the crazy bot and the ball follower. hell ya

import time
import traceback
import subprocess
from threading import Thread

from crazy_bot import CrazyBot
from ball_follower import BallFollower
from sensor_manager import SensorManager
from mapleIf import Maple
from motor_controller import MotorDriver

class MainBot:
    
    SEARCH, BALL_FOLLOW, SCORE = ("search", "ball_follow", "score")

    def __init__(self):
        self.maple = Maple()
        self.sensorManager = SensorManager(2300, self.maple)
        self.searchBot = CrazyBot(self.maple, self.sensorManager)
        self.ballFollower = BallFollower(self.maple, self.sensorManager)
        self.state = self.SEARCH
        self.stateStartTime = time.time()
        self.visionProcess = self.executeVisionProcess()
        self.driver = MotorDriver(self.maple)

    def executeVisionProcess(self):
        printVision = True

        def printOutput(out):
            for output_line in out:
                # print output_line
                pass

        p = subprocess.Popen('java -jar vision/maslab-vision.jar',
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
        if (printVision):
            visThread = Thread(target = printOutput, args = (iter(p.stdout.readline, b''),))
            visThread.start()
        time.sleep(3)
        return p

    def searchSetup(self):
        self.stateStartTime = time.time()
        self.searchBot.reset()
        return self.SEARCH

    def search(self):
        if self.sensorManager.vision.seeObject():
            if self.sensorManager.vision.seeBall() or (self.sensorManager.vision.seeReactor() and self.ballFollower.greenBallCount > 0):
                return self.ballFollowSetup()
        self.searchBot.mainIter()
        return self.SEARCH

    def ballFollowSetup(self):
        self.stateStartTime = time.time()
        self.driver.stopMotors()
        self.ballFollower.reset()
        return self.BALL_FOLLOW

    def ballFollow(self):
        if not self.sensorManager.vision.seeObject():
            return self.searchSetup()
        elif (not self.sensorManager.vision.seeBall()):
            # tODO remove this return
            if self.sensorManager.vision.seeReactor() and (self.ballFollower.greenBallCount == 0):
                # don't see any balls and don't have any balls
                return self.searchSetup()
        self.ballFollower.mainIter()
        return self.BALL_FOLLOW

    def mainLoop(self):
        while True:
            self.sensorManager.vision.getVisionInfo()
            # print self.state
            if self.state == self.SEARCH:
                self.state = self.search()
            elif self.state == self.BALL_FOLLOW:
                self.state = self.ballFollow()
            elif self.state == self.SCORE:
                self.state = self.score()
            time.sleep(0.01)

    def closeMaple(self):
        self.sensorManager.close()


if __name__ == '__main__':
    m = MainBot()
    try:
        m.mainLoop()
    except:
        traceback.print_exc()
        m.visionProcess.kill()
        m.closeMaple()


