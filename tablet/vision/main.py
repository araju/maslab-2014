# Handles the overall vision loop
# 1) Connect to camera
# 2) Read in frame
# 3) Resize frame and HSV thresh
# 4) Clean binary image and do blob detection
# 5) Process blob info
# 6) Publish list of balls with their distances and directions

import cv2
import process_frame as pf

def main():
	cap = connectToCamera()
	while (1):
		_, frame = cap.read()
		blobs = pf.findBlobs(frame) # blobs is a map of colors to lists of tuples (center, area)
		#balls,reactors = processBlobs(blobs)
		#publish(balls,reactors)
	

if __name__ == '__main__':
	main()
