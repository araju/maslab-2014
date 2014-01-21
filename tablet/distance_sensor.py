# represents the sonar sensors

class DistanceSensors(Sensor):
	def __init__(self, num, maple):
		self.numOfSensors = num
		self.distances = [0 for i in range(num)]
		self.maple = maple
		
		def updateValue(arg_list):
			time = arg_list[1] | (arg_list[2] << 8) # time in us
			distance = time * Math.pow(10,-6) * 170
			self.distances[arg_list[0]] = distance
		
		maple.registerCb(0x0B,updateValue)
