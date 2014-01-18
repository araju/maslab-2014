# control the motors

from mapleIf import Maple

class MotorDriver:

	def __init__(self):
		self.maple = Maple()

	def stopMotors():
		turnMotors(0)
		driveMotors(0)

	# only handles angles from -127 to 127.
	def turnMotors(theta):
		if theta < -127:
			theta = -127
		if theta > 127:
			theta = 127
		buf = [0x13,0x01,theta & 0xFF]
		this.maple.send(buf)

	def driveMotors(dist):
		if (dist > 255):
			dist = 255
		buf = [0x12,0x01,dist & 0xFF]
		this.maple.send(buf)