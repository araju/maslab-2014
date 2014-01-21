# odometry_reading.py
# Gets the current estimate of distance travelled and heading
# all the measurements are relative to the previous reset

class Odometry:

	def __init__(self, maple):
		self.distance = 0   # degrees
		self.direction = 0  # cm
		self.maple = maple
		def updateAngle(arg_list):
			self.direction = (arg_list[0] | (arg_list[1] << 8)) / 100.0
		def updateDistance(arg_list):
			self.distance = (arg_list[0] | (arg_list[1] << 8)) / 10.0 
		maple.registerCb(0x14, updateAngle)
		maple.registerCb(0x15, updateDistance)
