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
		self.pubSocket.setBlocking(0) # make it a non-blocking socket

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
	def publish(self, balls, reactors):
		ballMap = {"red":[],"green":[],"reactor":[]}
		for ball in balls:
			if ball[0] in ballMap.keys():
				ballMap[ball[0]].append((ball[1],ball[2]))
		ballMap["reactor"] = reactors
		ballMap["token"] = self.token

		data = json.dumps(ballMap)
		self.pubSocket.send(data)


	def close():
		self.pubSocket.close()

