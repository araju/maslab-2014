# test driving the motors

from motor_controller import MotorDriver
import time

driver = MotorDriver()

driver.turnMotors(90)
time.sleep(3)
driver.stopMotors()
##driver.close()
##time.sleep(3)
##driver.driveMotors(50) # in cm
