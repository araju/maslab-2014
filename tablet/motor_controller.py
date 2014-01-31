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
        # if theta < -127:
        #     theta = -127
        # if theta > 127:
        #     theta = 127
        buf = [0x13,0x02,int(theta) & 0xFF, (int(theta) >> 8) & 0xFF ]
        self.maple.send(buf)

    def driveBiasMotors(self,dist, bias):
        if (dist > 127):
            dist = 127
        elif (dist < -127):
            dist = -127

        if (bias > 127):
            dist = 127
        elif (bias < -127):
            bias = -127


        buf = [0x12,0x02,int(dist) & 0xFF, int(bias) & 0xFF]
        self.maple.send(buf)

    def driveMotors(self,dist):
        if (dist > 127):
            dist = 127
        elif (dist < -127):
            dist = -127
            
        buf = [0x12,0x02,int(dist) & 0xFF, 0]
        self.maple.send(buf)

    def driveMotorPWM(self, pwmLeft, pwmRight):
        pwmLeft = max(min(pwmLeft, 127), -127)
        pwmRight = max(min(pwmRight, 127), -127)

        buf = [0x18, 0x02, int(pwmLeft) & 0xFF, int(pwmRight) & 0xFF]
        self.maple.send(buf)

    def dumpGreen(self):
        buf = [0x06, 0x02, 0x01]
        self.maple.send(buf)

    def dumpRed(self):
        buf = [0x07, 0x02, 0x01]
        self.maple.send(buf)

    def close(self):
        if (self.maple != None):
                self.maple.close()
