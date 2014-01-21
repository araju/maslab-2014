# wall following with the shirt range IR

# only assuming that there are two sensors, both on the right side
from motor_controller import MotorDriver
from mapleIf import Maple
from bump_sensor import BumpSensors
import time
import traceback



def turnLeft(driver):
        driver.turnMotors(2)
        time.sleep(0.01)
        driver.driveMotors(2)
        time.sleep(0.05)

def turnRight(driver):
        driver.turnMotors(-2)
        time.sleep(0.01)
        driver.driveMotors(2)
        time.sleep(0.05)

def driveStraight(driver):
        driver.driveMotors(2)

maple = None
try:
        maple = Maple()
        driver = MotorDriver(maple)
        sensors = BumpSensors(2,maple)
        front = sensors.bumped[0]
        back = sensors.bumped[1]
        while 1:
                if (front and not back):
                        turnLeft(driver)
                elif not front and back:
                        turnRight(driver)
                elif not front and not back:
                        turnRight(driver)
                else:
                        driveStraight(driver)
                time.sleep(0.1)
except:
        traceback.print_exc()
finally:
        if maple != None:
                maple.close()
