# drives to the closest ball

import vision_consumer as vc
import motor_controller as mc

def main():
	vision = vc.VisionConsumer(2300)
	motor = mc.MotorDriver()
	while (True):
		point = vision.goal
		canDrive = turnToPoint(point)
		if (canDrive):
			driveToPoint(point)
		sleep(0.001)

# point = (direction, distance)
def turnToPoint(point, mc):
	if len(point) == 0:
		mc.stopMotors()
		return False
	theta = point[0]
	if abs(theta) < 10:
		return True
	else:
		mc.turnMotors(-theta)

def driveToPoint(point, mc):
	if len(point) == 0:
		mc.stopMotors()
		return
	dist = point[1]
	if (dist > 5):
		mc.driveMotors(dist)


if __name__ == '__main__':
    main()

