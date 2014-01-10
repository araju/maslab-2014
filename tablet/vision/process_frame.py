import cv2
import numpy as np


# define range of blue color in HSV
lower_blue = np.array([90,100,50])
upper_blue = np.array([115,255,255])

#define range of red color in HSV
lower_red = np.array([0,100,10])
upper_red = np.array([15,255,255])

# define range of green color in HSV
lower_green = np.array([55,80,10])
upper_green = np.array([90,255,255])

clean_kernel = np.ones((5,5),np.uint8)
contourAreaThresh = 50


# Processes raw frame to output the centers and sizes of colored blobs
# this includes balls and walls/reactors and QR codes
#
# TODO: detect QR codes
def processFrame(frame):
	# Threshold the HSV image to get colors
    maskRed = cv2.inRange(hsv, lower_red, upper_red)
    maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)
    maskGreen = cv2.inRange(hsv, lower_green, upper_green)

    # process mask to clean noise
    cleanedRed = cv2.morphologyEx(maskRed, cv2.MORPH_OPEN, clean_kernel)
    cleanedBlue = cv2.morphologyEx(maskBlue, cv2.MORPH_OPEN, clean_kernel)
    cleanedGreen = cv2.morphologyEx(maskGreen, cv2.MORPH_OPEN, clean_kernel)

    blobs = {}
    blobs['red'] = findBlobs(cleanedRed)
    blobs['blue'] = findBlobs(cleanedBlue)
    blobs['green'] = findBlobs(cleanedGreen)

    return blobs

# returns list of blobs with (center, area)
 def findBlobs(binary_img):
 	contours,heirarchy = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ret = []
    for cnt in contours:
        if cv2.contourArea(c) > contourAreaThresh:
        	rx,ry,rw,rh = cv2.boundingRect(cnt)
        	ret.append((rx + (rw / 2), ry + (rh / 2)), cv2.contourArea(cnt))





