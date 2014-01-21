# represents the short range IRs

class BumpSensors():
	def __init__(self, num, maple):
		self.numOfSensors = num
		self.bumped = [False for i in range(num)]
		self.maple = maple
		# arg_list = [sensor id, bumped? (0 or 1, 0 = bumped)]
		def updateValue(arg_list):
			self.bumped[arg_list[0]] = (arg_list[1] == 0)

		maple.registerCb(0x14, updateValue)

	
