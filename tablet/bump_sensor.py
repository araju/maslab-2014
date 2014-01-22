# represents the short range IRs

class BumpSensors():
	def __init__(self, num, maple):
		self.numOfSensors = num
		self.bumped = [False for i in range(num)]
		self.maple = maple
		# arg_list = [bumped bit then id bits]
		def updateValue(arg_list):

			idx = arg_list[1] & 0x7F
			value = arg_list[1] & 0x80

			# print idx, value
			self.bumped[idx] = (value >> 7 == 1)
			# print self.bumped

		maple.registerCb(0x16, updateValue)

	
