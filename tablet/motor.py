# Low-level control of each Motor
# 0 = Left, 1 = Right

class Motor:
	def __init__(self, id):
		self.motorID = id #ID = 0 = Left, ID = 1 = Right

	def setMotorPWM(self, pwm):
		#TODO: actually send the pwm somewhere
		if id == 0:
			cmdID = 0x00
		else:
			cmdID = 0x01
		buf = [cmdID, 0x01, pwm & 0xFF]
		maple.send(buf)