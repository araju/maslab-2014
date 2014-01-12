# Processes the blob info to give real world info about the balls and walls

#TODO: find conversion factors (NEED TO CALIBRATE)
yConversion = 0
xConversion = 0
sizeConversion = 0


# blobs = map from colors to lists of tuples (center, size)
# output = two things:
# 	- balls: list of tuples (ball color, direction, distance) in order of distance
#	- reactors: list of tuples (direction, distance)
def processBlobs(blobs):
	pass