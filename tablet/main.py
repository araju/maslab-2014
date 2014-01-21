# main.py
# This is the main loop for the robot
# 
# Order of operations:
# 1. Get sensor data
# 2. Check if we are stuck.
# 3. State transition
# 4. Do an action

import time
import BotClientCommunicator
import SensorManager
from states import *

def main():
	sensors = {} # where we copy sensor data to at the start of each loop
	# TODO: define sensors objs and add the keys to the sensor map
	state = States.IDLE
	botClient = BotClientCommunicator() # TODO: actually make this class
	sensorManager = SensorManager() # TODO: make this class
	while (not botClient.recvStartSignal):
		time.sleep(0.1) # wait for the start signal

	state = States.EXPLORE

	## Start Main Loop ##
	while (not botClient.recvStopSignal):
		sensors = sensorManager.getSensorReadings()
		if (isStuck(sensors)): # TODO: figure out how to deal with being stuck
			state = States.STUCK
			getOutOfStuck()
			continue
		state = stateTransition(state, sensors) #update the state based on the sensors
		performAction(state, sensors)


def isStuck(sensors):
	print "unimplemented method: isStuck"
	return False

def getOutOfStuck(): # might not need this here, could put it in sensors
	print "unimplemented method: getOutOfStuck"

# see wiki page for a rough diagram of how we transition states
def stateTransition(currentState, sensors):
	print "unimplemented method: stateTransition"
	if currentState == States.IDLE:
		pass
	elif currentState == States.EXPLORE:
		pass
	elif currentState == States.GO_TO_OBJ:
		pass
	elif currentState == States.WALL_FOLLOW:
		pass
	elif currentState == States.RETURN_TO_WALL:
		pass
	elif currentState == States.DROP_RED:
		pass
	elif currentState == States.SCORE:
		pass
	elif currentState == States.STUCK:
		pass
	else:
		print "Unknown State!!!"

def performAction(state, sensors):
	print "unimplemented method: performAction"
	#TODO: add some logic that might make this more discriminatory
	# for instance, might not want to do the same thing every time we 
	# are in a state. e.g. when we are in a score or go_to_ogj state
	# but we dont have any balls.

	# for now, make this a dumb method. performs the action for the state
	States.getStateActions()[state](sensors)



if __name__ == '__main__':
	main()
