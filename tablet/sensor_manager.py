#sensor_manager.py
# keeps a list of sensors and updates the values of their outputs
# included with that is the vision output

import copy
import time
from threading import Thread
from distance_sensor import DistanceSensors
from bump_sensor import BumpSensors
from vision_consumer import VisionConsumer
from odometry_reading import Odometry

class SensorManager:

    def __init__(self, port, maple):
        distanceNum = 6
        shortRangeNum = 6

        self.maple = maple
        self.sonars = DistanceSensors(distanceNum, maple)
        self.bumps = BumpSensors(shortRangeNum, maple)
        self.odo = Odometry(maple)
        self.visionConsumer = VisionConsumer(port)
        self.vision = VisionInfo(self.visionConsumer)
        self.currentSensorReadings = {
            "sonar" : [0 for i in range(distanceNum)],
            "shortIR" : [0 for i in range(shortRangeNum)],
            "odometry" : {"direction" : 0.0, "distance" : 0.0},
            "vision" : {"red" : [], "green" : [], "blue" : [], "reactor" : [] }
        }
        self.visionConsumer.startServer()
        self.mapleRead = True
        readThread = Thread(target = self.readMaple)
        readThread.start()


    def readMaple(self):
        while self.mapleRead:
            self.maple.periodic_task()
            time.sleep(0.01)


    def close(self):
        self.mapleRead = False
        self.visionConsumer.close()
        

    def getSensorReadings(self):
        self.currentSensorReadings["sonar"] = copy.copy(self.distanceSensors.distances)
        self.currentSensorReadings["shortIR"] = copy.copy(self.shortRangeIRs.bumped)
        self.currentSensorReadings["vision"] = copy.deepcopy(self.visionConsumer)
        self.currentSensorReadings["odometry"]["direction"] = self.odometry.direction
        self.currentSensorReadings["odometry"]["distance"] = self.odometry.distance
        return self.currentSensorReadings


####################################################


# essentially a copy of the info in vision_consumer, but used as a copy
# a bit ugly, but I don't want to deal with locks and stuff
class VisionInfo:
    def __init__(self, visCom):
        self.visionConsumer = visCom

        self.goalBall = [] # direction, distance, color of goal
        self.goalReactor = []
        self.goalYellow = []
        self.ballMap = {"red" : [], "green" : [], "blue" : [], "reactors" : [], "yellow" : [], "wallEnds" : []}

    # call this once a loop to get consistent vision info for the entire loop
    # helps avoid concurrency issues
    def getVisionInfo(self):
        self.ballMap = copy.copy(self.visionConsumer.ballMap)
        green = copy.copy(self.ballMap["green"])
        green.append("green")
        red = copy.copy(self.ballMap["red"])
        red.append("red")
        if len(red) == 1 and len(green) == 1:
            self.goalBall = []
        elif len(red) > len(green):
            self.goalBall = red
        elif len(green) > len(red):
            self.goalBall = green
        elif abs(red[1] - green[1]) > 10: # big diff in distance
            if (red[1] < green[1]):
                self.goalBall = red
            else:
                self.goalBall = green
        else: # small diff in distance
            if abs(red[0]) < abs(green[0]): # red more centralized
                self.goalBall = red
            else:
                self.goalBall = green

        if len(self.ballMap["reactors"]) > 0:
            self.goalReactor = self.ballMap["reactors"]
        else:
            self.goalReactor = []

        if "yellow" in self.ballMap.keys() and len(self.ballMap["yellow"]) > 0:
            self.goalYellow = self.ballMap["yellow"]
        else:
            self.goalYellow = []


    def seeGreenBall(self):
        return len(self.ballMap["green"]) > 0

    def seeRedBall(self):
        return len(self.ballMap["red"]) > 0

    def seeReactor(self):
        return len(self.goalReactor) > 0

    def seeYellowWall(self):
        return len(self.goalYellow) > 0

    def seeBall(self):
        return self.seeGreenBall() or self.seeRedBall()

    def seeObject(self):
        return self.seeBall() or self.seeReactor() or self.seeYellowWall()

    # def getWallY(self):
    #     if len(self.ballMap["blue"]) > 0:
    #         return self.ballMap["blue"][1]
    #     else:
    #         return 0