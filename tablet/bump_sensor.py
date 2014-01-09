class BumpSensors(Sensor):
	def __init__(self, num):
		self.numOfSensors = num
		self.bumped = [False for i in range(num)]

	# arg_list = [sensor id, bumped? (0 or 1)]
	def updateValue(self, arg_list):
		self.bumped[arg_list[0]] = (arg_list[1] == 1)
