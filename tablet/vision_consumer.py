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
		this.goal = () # direction, distance of goal
		thread = Thread(target = self.startServer)
		thread.start()

	# TODO: handle the reactors!!!!
	def startServer(self):
		while True:
			clisock, (remhost, remport) = srvsock.accept()
	  		json = clisock.recv(4096)
	  		ballMap = json.loads(json)
	  		green = ballMap["green"]
	  		red = ballMap["red"]
	  		if len(red) == 0 and len(green) == 0:
	  			this.goal = ()
	  		elif len(red) > len(green):
	  			this.goal = red
	  		elif len(green) > len(red):
	  			this.goal = green
	  		elif (red[1] < green[1]):
	  			this.goal = red
	  		else:
	  			this.goal = green






