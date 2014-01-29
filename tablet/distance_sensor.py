# represents the sonar sensors

class DistanceSensors():
	def __init__(self, num, maple):
		self.numOfSensors = num
		self.distances = [0 for i in range(num)]
		self.maple = maple
		
		def updateValue(arg_list):
			# low pass the values
			# self.distances[int(arg_list[1])] = 0.5*(int(arg_list[2]) | (int(arg_list[3]) << 8)) + 0.5*self.distances[int(arg_list[1])] # distance in cm
			self.distances[int(arg_list[1])] = (int(arg_list[2]) | (int(arg_list[3]) << 8)) # no low pass, check if we need it
			# print "%2.3f %2.3f %2.3f %2.3f %2.3f %2.3f" % (self.distances[0], self.distances[1], self.distances[2], self.distances[3], self.distances[4], self.distances[5])
		
		maple.registerCb(0x0B,updateValue)
