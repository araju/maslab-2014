class BumpSensors(Sensor):
	def __init__(self, num, maple):
		self.numOfSensors = num
		self.bumped = [False for i in range(num)]
		self.maple = maple
		maple.registerCb(0x14, updateValue)

	# arg_list = [sensor id, bumped? (0 or 1)]
	def updateValue(self, arg_list):
		self.bumped[arg_list[0]] = (arg_list[1] == 1)
