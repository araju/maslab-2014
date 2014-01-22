# consumes vision data and turns towards balls 
# written for the mock competition #1, but hopfulle can be used later too

import json
import socket
from threading import Thread


class VisionConsumer:

	# following denote the closest ball/reactor. given as a [direction, distance]
	closestGreen = []
	closestRed = []
	closestReactor = []

	def __init__(self, port):
		self.svrSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.svrSock.bind(('localhost', 2300))
		self.svrSock.listen(5)
		self.goal = () # direction, distance of goal
		self.ballMap = {"red" : [], "green" : [], "reactor" : []}
		thread = Thread(target = self.startServer)
		thread.start()

	# TODO: handle the reactors!!!!
	def startServer(self):
		while True:
			clisock, (remhost, remport) = srvsock.accept()
	  		json = clisock.recv(4096)
	  		self.ballMap = json.loads(json)
	  		green = self.ballMap["green"]
	  		red = self.ballMap["red"]
	  		if len(red) == 0 and len(green) == 0:
	  			self.goal = ()
	  		elif len(red) > len(green):
	  			self.goal = red
	  		elif len(green) > len(red):
	  			self.goal = green
	  		elif (red[1] < green[1]):
	  			self.goal = red
	  		else:
	  			self.goal = green







