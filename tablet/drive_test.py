# test driving the motors

from motor_controller import MotorDriver
import time
from mapleIf import Maple
from music import playMusic
import traceback
from distance_sensor import DistanceSensors
from bump_sensor import BumpSensors
import subprocess
from threading import Thread
from sensor_manager import SensorManager


# def executeVisionThread():
#     def printOutput(out):
#         for output_line in out:
#             print output_line

#     p = subprocess.Popen('java -jar vision/maslab-vision.jar',
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.STDOUT)
#     visThread = Thread(target = printOutput, args = (iter(p.stdout.readline, b''),))
#     visThread.start()
#     return (visThread, p)

# thread, process = executeVisionThread()
# time.sleep(10)
# process.kill()
# try:
# 	playMusic.play()
# 	time.sleep(10)
# except:
# 	traceback.print_exc()


maple = Maple()
driver = MotorDriver(maple)
sensorManager = SensorManager(2300, maple)
time.sleep(0.5)
driver.driveMotors(30)
# driver.dumpGreen()
# driver.dumpRed()
# driver.turnMotors(90)
# time.sleep(5)
# dist = DistanceSensors(6,maple)
# bumps = BumpSensors(6,maple)
run = True
try:
    while run:
        # print "get info"
        maple.periodic_task()
        # print "Direction: ", sensorManager.odo.direction
        time.sleep(0.001)
except:
    run = False
    traceback.print_exc()


# driver.driveMotors(20)
# time.sleep(5)
# driver.turnMotors(90)



# driver.turnMotors(90)
# time.sleep(3)
# driver.stopMotors()
##driver.close()
##time.sleep(3)
##driver.driveMotors(50) # in cm
