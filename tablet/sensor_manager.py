#sensor_manager.py
# keeps a list of sensors and updates the values of their outputs
# included with that is the vision output

import copy
import time
from distance_sensor import DistanceSensors
from bump_sensor import BumpSensors
from vision_consumer import VisionConsumer
from odometry_reading import Odometry

class SensorManager:

	def __init__(self, port, maple):
		distanceNum = 4
		shortRangeNum = 6

		self.maple = maple
		self.distanceSensors = DistanceSensors(distanceNum, maple)
		self.shortRangeIRs = BumpSensors(shortRangeNum, maple)
		self.odometry = Odometry(maple)
		self.visionConsumer = VisionConsumer(port)
		self.currentSensorReadings = {
			"sonar" : [0 for i in range(distanceNum)],
			"shortIR" : [0 for i in range(shortRangeNum)],
			"odometry" : {"direction" : 0.0, "distance" : 0.0}
			"vision" : {"red" : [], "green" : [], "blue" : [], "reactor" : [] }
		}

		# starts receiving info from the maple
		def readMapleInfo():
			while (1):
				self.maple.periodicTask()
				time.sleep(0.1)

		readThread = Thread(target = readMapleInfo)
		readThread.start()




	def getSensorReadings(self):
		self.currentSensorReadings["sonar"] = copy.copy(self.distanceSensors.distances)
		self.currentSensorReadings["shortIR"] = copy.copy(self.shortRangeIRs.bumped)
		self.currentSensorReadings["vision"] = copy.deepcopy(self.visionConsumer)
		self.currentSensorReadings["odometry"]["direction"] = self.odometry.direction
		self.currentSensorReadings["odometry"]["distance"] = self.odometry.distance
		return self.currentSensorReadings