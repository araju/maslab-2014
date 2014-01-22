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
from distance_sensor import DistanceSensors
# import msvcrt

class WallFollow:
    turnTo, goAway, straight, start, cornerTurn, cornerStraight = \
        ("turnTo", "goAway", "straight", "start", "cornerTurn", "cornerStraight")


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
        time.sleep(0.01)

maple = None
driver = None
try:
    maple = Maple()
    driver = MotorDriver(maple)
    bumps = BumpSensors(4,maple)
    odo = Odo(maple)
    pwm = pwmSense.PWMSense(maple)
    sonars = DistanceSensors(4,maple)
    count = 0

    BIAS_K = 2.0
    DIST_OFF = 10.0
    DIST_K = 1.0

    thread = Thread(target = readMaple, args = (maple,))
    thread.start()
    time.sleep(0.1) # just let the thread get started
    wfState = WallFollow.start
    prevDist = sonars.distances[3]
    # while not msvcrt.kbhit():
    while True:
        front = bumps.bumped[3]
        back = bumps.bumped[2]
        dist = sonars.distances[3]
        
        # print dist

        dDist = dist - prevDist
        biasOffset = dDist * BIAS_K
        distSetPoint = 10
        distErr =  10 - dist
        distPropGain = distErr * DIST_K

        # print front, back, wfState, 
        if not wfState in [WallFollow.cornerTurn, WallFollow.cornerStraight]:
            if front and not back:
                newState = WallFollow.goAway
            if not front and back:
                newState = WallFollow.turnTo
            if not front and not back:
                newState = WallFollow.turnTo
            if front and back:
                newState = WallFollow.straight
            if not front and distErr < -30:
                newState = WallFollow.cornerTurn
        elif wfState in [WallFollow.cornerTurn, WallFollow.cornerStraight]:
            if ((wfState == WallFollow.cornerTurn and dist < 15) or (front and not back)) and \
                    odo.direction > 20:
                newState = WallFollow.cornerStraight
            if front and back:
                newState = WallFollow.straight

        print front, back, newState, biasOffset, odo.distance, distErr, dist, odo.direction

        if newState != wfState or odo.distance > 10:
            if biasOffset < -15:
                biasOffset = -15
            elif biasOffset > 15:
                biasOffset = 15
            wfState = newState
            if wfState == WallFollow.straight:
                driver.driveBiasMotors(15,-biasOffset + distPropGain)
            elif wfState == WallFollow.goAway:
                driver.driveBiasMotors(15, 2 + biasOffset - distPropGain)
            elif wfState == WallFollow.turnTo:
                driver.driveBiasMotors(15, -10 - biasOffset + distPropGain)
            elif wfState == WallFollow.cornerTurn:
                print 'Corner Turn'
                driver.driveBiasMotors(15, -20)
            elif wfState == WallFollow.cornerStraight:
                print 'Drive Straight Dude'
                driver.driveBiasMotors(15, 0)
        prevDist = dist

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
    thread.stop()
except:
    traceback.print_exc()
finally:
    if driver != None:
        driver.stopMotors()
    if maple != None:
        maple.close()
