import math

# Processes the blob info to give real world info about the balls and walls

# conversion factors found through calibration

# blobs = map from colors to lists of tuples (center (x,y) in img coords, size)
# output = two things:
# 	- balls: map of colors to lists of tuples (direction, distance) in order of distance
#	- reactors: list of tuples (direction, distance)
def processBlobs(blobs):
	balls = {}
	for color in blobs.keys():
		balls[color] = []
		for (x,y),size in blobs[color]:
			direction = calcDirection(x)
			distance = calcDistance(x,y)
			balls[color].append((direction,distance))
		sorted(balls[color], key=lambda ball: ball[1]) # sort by distance

	return balls, [] # TODO : find reactors!!!

def calcDirection(x):
	theta = math.degrees(math.atan(abs(x - 320) / 340))
	return theta

def calcDistance(x,y):
	zDist = 3500 / (y - 255)