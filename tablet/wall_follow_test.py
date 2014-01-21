# wall following with the shirt range IR

# only assuming that there are two sensors, both on the right side
from motor_controller import MotorDriver
from mapleIf import Maple
from bump_sensor import BumpSensors
import time
import traceback
from threading import Thread



def turnLeft(driver):
        driver.turnMotors(5)
        # time.sleep(0.5)
        # driver.driveMotors(2)
        # time.sleep(0.2)

def turnRight(driver):
        driver.turnMotors(-5)
        # time.sleep(0.5)
        # driver.driveMotors(2)
        # time.sleep(0.2)

def driveStraight(driver):
        driver.driveMotors(2)

def readMaple(maple):
        while 1:
                maple.periodic_task()
                time.sleep(0.05)

maple = None
driver = None
try:
        maple = Maple()
        driver = MotorDriver(maple)
        sensors = BumpSensors(4,maple)
        count = 0
        thread = Thread(target = readMaple, args = (maple,))
        thread.start()
        while 1:
                # maple.periodic_task()
                front = sensors.bumped[3]
                back = sensors.bumped[2]
                print "Front: ", front, "  Back: ", back
                if (count % 100 == 0):
                        print sensors.bumped
                        count = 0
                if front and (not back):
                        turnLeft(driver)

                elif not front and back:
                        turnRight(driver)
                elif not front and not back:
                        turnRight(driver)
                else:
                        driveStraight(driver)
                time.sleep(0.1)
                count += 1
except:
        traceback.print_exc()
finally:
        if driver != None:
                driver.stopMotors()
        if maple != None:
                maple.close()
