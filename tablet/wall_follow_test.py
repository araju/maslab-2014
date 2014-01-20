# wall following with the shirt range IR

# only assuming that there are two sensors, both on the right side
from motor_controller import MotorDriver
from bump_sensor import BumpSensor
import time

maple = Maple()
driver = MotorDriver(maple)
sensors = BumpSensors(2,maple)

while 1:
	if (front and not back):
		turnLeft()
	elif not front and back:
		turnRight()
	elif not front and not back:
		turnRight()
	else:
		driveStraight()
	time.sleep(0.1)

def turnLeft():
	driver.turnMotors(2)
	time.sleep(0.01)
	driver.driveMotors(2)
	time.sleep(0.05)

def turnRight():
	driver.turnMotors(-2)
	time.sleep(0.01)
	driver.driveMotors(2)
	time.sleep(0.05)

def driveStraight():
	driver.driveMotors(2)
