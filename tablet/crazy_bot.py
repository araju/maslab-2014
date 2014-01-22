# crazy_bot.py
# This shit is crazy. Bot goes in random directions and turns when it hits a wall

import time
from mapleIf import Maple
from threading import Thread
from bump_sensor import BumpSensors
from distance_sensor import DistanceSensors
from odometry_reading import Odometry
from motor_controller import MotorDriver

class CrazyBot:
    MOVE_FORWARD, BACK_UP, SEARCH_DIRECTION, TURN_TO_DIR = ("moveForward", "backup", "search", "turnToDir")

    def __init__(self):
        self.state = self.SEARCH_DIRECTION
        self.maple = Maple()
        self.driver = MotorDriver(self.maple)
        self.odo = Odometry(self.maple)
        self.bumps = BumpSensors(4,self.maple)
        self.sonars = DistanceSensors(4,self.maple)
        def readMaple():
            while 1:
                self.maple.periodic_task()
                time.sleep(0.01)
        self.t = Thread(target = readMaple)
        self.t.start()
        self.distances = [0 for i in range(36)]

    def moveForward(self):
        pass

    def backUp(self):
        pass

    def searchDirection(self):
        print self.searchDirection.distances
        

    searchDirection.distances = []
    def turnToDir(self):
        pass

    def mainLoop(self):
        while True:
            if self.state == self.MOVE_FORWARD:
                self.state = self.moveForward()
            elif self.state == self.BACK_UP:
                self.state = self.backUp()
            elif self.state == self.SEARCH_DIRECTION:
                self.state = self.searchDirection()
            elif self.state == self.TURN_TO_DIR:
                self.state = self.turnToDir()



if __name__ == '__main__':
    c = CrazyBot()
    c.mainLoop()
