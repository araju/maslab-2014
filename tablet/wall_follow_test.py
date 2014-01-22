# wall following with the shirt range IR

# only assuming that there are two sensors, both on the right side
from motor_controller import MotorDriver
from mapleIf import Maple
from bump_sensor import BumpSensors
from odometry_reading import Odometry as Odo
import time
import traceback
from threading import Thread
import pwmSense
class WallFollow:
    turnTo, goAway, straight = range(3)


def turnLeft(driver):
        # driver.driveBiasMotors(10,5)
        # driver.driveMotors(10,5)
        driver.turnMotors(5)
        # time.sleep(0.5)
        # driver.driveMotors(2)
        # time.sleep(0.2)

def turnRight(driver):
        # driver.driveBiasMotors(10,-5)
        # driver.driveMotors(10)
        # time.sleep(0.5)
        driver.turnMotors(-5)
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
    odo = Odo(maple)
    pwm = pwmSense.PWMSense(maple)

    count = 0
    thread = Thread(target = readMaple, args = (maple,))
    thread.start()
    wfState = WallFollow.straight
    while 1:
        front = sensors.bumped[3]
        back = sensors.bumped[2]

        newState = wfState

        print front, back, wfState, odo.distance, pwm.pwmChannels
        if front and not back:
            newState = WallFollow.goAway
        if not front and back:
            newState = WallFollow.turnTo
        if not front and not back:
            newState = WallFollow.turnTo
        if front and back:
            newState = WallFollow.straight

        if newState != wfState or odo.distance > 10:            
            wfState = newState
            if wfState == WallFollow.straight:
                driver.driveMotors(15)
            elif wfState == WallFollow.goAway:
                driver.driveBiasMotors(15, 0)
            elif wfState == WallFollow.turnTo:
                driver.driveBiasMotors(15, 0)

        # front = sensors.bumped[3]
        # back = sensors.bumped[2]
        # print "Front: ", front, "  Back: ", back
        # if (count % 100 == 0):
        #         print sensors.bumped
        #         count = 0
        # if front and (not back):
        #         turnLeft(driver)

        # elif not front and back:
        #         turnRight(driver)
        # elif not front and not back:
        #         turnRight(driver)
        # else:
        #         driveStraight(driver)
        time.sleep(0.1)
        count += 1
except:
    traceback.print_exc()
finally:
    if driver != None:
        driver.stopMotors()
    if maple != None:
        maple.close()
