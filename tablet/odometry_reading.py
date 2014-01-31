# odometry_reading.py
# Gets the current estimate of distance travelled and heading
# all the measurements are relative to the previous reset
import time

class Odometry:

	def __init__(self, maple):
		self.distance = 0   # degrees
		self.direction = 0  # cm
		self.maple = maple
		self.lastReading = None
		self.lastReadingTime = None
		self.angularRate = 0

		def updateAngle(arg_list):
			self.direction = (arg_list[1] | (arg_list[2] << 8)) / 100.0
			if not self.lastReading is None:
				dt = time.time() - self.lastReadingTime
				dTheta = self.lastReading - self.direction
				self.angularRate = self.angularRate * .75 + .25 * dTheta/dt
			self.lastReadingTime = time.time()
			self.lastReading = self.direction
			# if self.direction > 180:
			# 	self.direction -= 360
			# print self.direction, self.angularRate

		def updateDistance(arg_list):
			self.distance = (arg_list[1] | (arg_list[2] << 8)) / 10.0 
			if self.distance > (2**15)/10:
				self.distance -= 65535/10.0
			# print self.distance
		
		maple.registerCb(0x14, updateAngle)
		maple.registerCb(0x15, updateDistance)
