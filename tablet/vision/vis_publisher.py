# vis_publisher.py
# Publishes the vision info to some socket
# Uses similar json protocol as BotClient:
# {"token":<yourtokenhere>, <field_identifier>:[<somestring>,<somestring>]}done\n

import socket
import json

class VisPublisher:
	def __init__(self, port, token):
		self.port = port
		self.token = str(token)
		self.pubSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.pubSocket.connect(('localhost',port))
		self.pubSocket.setblocking(0) # make it a non-blocking socket

	'''
	## OLD - balls - list of tuples (color, direction, distance)
	balls = map of color to list of tuples (direction, distance), sorted by distance
	reactors - list of tuples (direction, distance)
	
	publishing json in the form:
	{
		"token": <ourtokenhere>
		<ball_color>:[[<direction>,<distance>],...]
		"reactor":[[<direction>,<distance>],...]
	}
	'''
	# TODO: change to only sending the closest ball
	def publish(self, balls, reactors):
		# ballMap = {"red":[],"green":[],"reactor":[]}
		# for ball in balls:
		# 	if ball[0] in ballMap.keys():
		# 		ballMap[ball[0]].append((ball[1],ball[2]))
		# ballMap["reactor"] = reactors
		# ballMap["token"] = self.token

		sendMap = {}
		for color in balls.keys():
			if (len(balls[color]) > 0):
				sendMap[color] = balls[color][0]
			else:
				sendMap[color] = []

		if (len(reactors) > 0):
			sendMap["reactor"] = reactors[0]
		else:
			sendMap["reactor"] = []
		if 
		sendMap["token"] = self.token

		data = json.dumps(sendMap)
		self.pubSocket.send(data + "\n")


	def close():
		self.pubSocket.close()

