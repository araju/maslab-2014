# test driving the motors

from motor_controller import MotorDriver
import time

driver = MotorDriver()

driver.turnMotors(90)
driver.stopMotors()
time.sleep(3)
driver.driveMotors(50) # in cm