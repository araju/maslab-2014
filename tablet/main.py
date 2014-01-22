# main.py
# This is the main loop for the robot
# 
# Order of operations:
# 1. Get sensor data
# 2. Check if we are stuck.
# 3. State transition
# 4. Do an action

import time
from pygame import mixer

import BotClientCommunicator
import SensorManager
from states import *


class Main:

	def __init__(self):
		# init variables
		self.botClientHost = "localhost"
		self.botClientPort = 9876
		self.visionPort = 2300
		self.sensors = {} # where we copy sensor data to at the start of each loop
		self.state = States.IDLE
		self.maple  = Maple()
		self.botClient = BotClientCommunicator(botClientHost,botClientPort)
		self.sensorManager = SensorManager(visionPort, maple)
		self.redBallCount = 0
		self.greenBallCount = 0


	def mainLoop(self):
		while (not self.botClient.recvStartSignal):
			time.sleep(0.1) # wait for the start signal

		startMusic()
		self.state = States.EXPLORE

		## Start Main Loop ##
		while (not self.botClient.recvStopSignal):
			self.sensors = self.sensorManager.getSensorReadings()
			if (self.isStuck()): # TODO: figure out how to deal with being stuck
				self.state = States.STUCK
				self.getOutOfStuck()
				continue
			self.state = self.stateTransition() #update the state based on the sensors
			self.performAction()

		stopMusic()


	def startMusic():
		mixer.init()
		mixer.music.load('Castle_of_Glass.mp3')
		mixer.music.play()

	def stopMusic():
		mixer.music.stop()


	def isStuck(self):
		print "unimplemented method: isStuck"
		return False

	def getOutOfStuck(self): # might not need this here, could put it in sensors
		print "unimplemented method: getOutOfStuck"

	# see wiki page for a rough diagram of how we transition states
	def stateTransition(self):
		print "unimplemented method: stateTransition"
		if self.state == States.IDLE:
			return States.IDLE
		elif self.state == States.EXPLORE:
			if (self.foundBall()):
				return States.GO_TO_BALL
			elif self.foundReactor() and self.greenBallCount > 0:
				return States.GO_TO_REACTOR
			elif self.exploreCompleted():
				return States.RETURN_TO_WALL
			else:
				return States.EXPLORE
		elif self.state == States.GO_TO_BALL:
			if (self.foundBall()): # the ball is still in view, or there is another ball in view
				return States.GO_TO_BALL
			elif self.foundReactor():
				return States.GO_TO_REACTOR
			else:
				return States.EXPLORE
		elif self.state == States.WALL_FOLLOW:
			if (self.foundBall()):
				return States.GO_TO_BALL
			elif self.foundReactor():
				return States.GO_TO_REACTOR
			elif self.lostWall():
				return States.RETURN_TO_WALL
			else:
				return States.WALL_FOLLOW
		elif self.state == States.RETURN_TO_WALL:
			if self.lostWall(): # still lost
				return States.RETURN_TO_WALL
			else:
				return States.WALL_FOLLOW
		elif self.state == States.DROP_RED:
			return self.EXPLORE # assumes that we've already dropped the balls
		elif self.state == States.SCORE:
			return States.EXPLORE # assumes we've already dropped the balls
		elif self.state == States.STUCK:
			if self.isStuck(): # we are still stuck
				return States.STUCK
			else:
				return States.EXPLORE
		else:
			print "Unknown State!!!: ", self.state

	def performAction(self):
		print "unimplemented method: performAction"
		#TODO: add some logic that might make this more discriminatory
		# for instance, might not want to do the same thing every time we 
		# are in a state.

		# for now, make this a dumb method. performs the action for the state
		States.getStateActions()[self.state](self.sensors)


	def foundBall(self):
		ballMap = self.sensors["vision"]
		return (len(ballMap["red"]) > 0 or len(ballMap["green"]) > 0)

	def foundReactor(self):
		return (len(self.sensors["vision"]["reactors"]) > 0)

	def exploreCompleted(self):
		print "unimplemented method: exploreCompleted"

	def lostWall(self):
		print "unimplemented method: lostWall"
		return False






############### START MAIN ##################

def main():
	m = Main()
	m.mainLoop()

################### END MAIN ######################

if __name__ == '__main__':
	main()
