# control the motors

from mapleIf import Maple

class MotorDriver:

	def __init__(self,m):
		self.maple = m

        def read(self):
                def testCb(args):
                        print 'Received: ', args
                
                        

	def stopMotors(self):
		self.turnMotors(0)
		self.driveMotors(0)

	# only handles angles from -127 to 127.
	def turnMotors(self,theta):
		if theta < -127:
			theta = -127
		if theta > 127:
			theta = 127
		buf = [0x13,0x01,theta & 0xFF]
		self.maple.send(buf)

	def driveMotors(self,dist):
		if (dist > 255):
			dist = 255
		buf = [0x12,0x01,dist & 0xFF]
		self.maple.send(buf)

	def close(self):
                if (self.maple != None):
                        self.maple.close()
