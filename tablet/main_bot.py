# main_bot.py
# switches between the crazy bot and the ball follower. hell ya

import time
import traceback

from crazy_bot import CrazyBot
from ball_follower import BallFollower
from mapleIf import Maple

class MainBot:
    
    SEARCH, BALL_FOLLOW = ("search", "ball_follow")

    def __init__(self):
        self.maple = Maple()
        self.sensorManager = SensorManager(self.maple, 2300)
        self.searchBot = CrazyBot(self.maple, self.sensorManager)
        self.ballFollower = BallFollower(self.maple, self.sensorManager)
        self.state = SEARCH
        self.stateStartTime = time.time()
        self.greenBallCount = 0
        self.redBallCount = 0

    def searchSetup(self):
        self.stateStartTime = time.time()
        self.searchBot.reset()
        return self.SEARCH

    def search(self):
        if self.sensorManager.vision.seeObject():
            return self.ballFollowSetup()
        self.searchBot.mainIter()
        return self.SEARCH

    def ballFollowSetup(self):
        self.stateStartTime = time.time()
        self.ballFollower.reset()
        return self.BALL_FOLLOW

    def ballFollow(self):
        if not self.sensorManager.vision.seeObject():
            return self.searchSetup()
        elif (not self.sensorManager.vision.seeBall()) and (self.greenBallCount + self.redBallCount == 0):
            # don't see any balls and don't have any balls
            return self.searchSetup()
        else:
            self.ballFollow.mainIter()
            return self.BALL_FOLLOW

    def mainLoop(self):
        while True:
            if self.state == self.SEARCH:
                self.state = self.search()
            elif self.state == self.BALL_FOLLOW:
                self.state = self.ballFollow()
            time.sleep(0.01)

    def closeMaple(self):
        self.sensorManager.close()


if __name__ == '__main__':
    m = MainBot()
    try:
        m.mainLoop()
    except:
        traceback.print_exc()
        m.closeMaple()


