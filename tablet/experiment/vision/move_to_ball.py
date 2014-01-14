# draw bounding box around balls in video feed

import cv2
import numpy as np
import time

for i in range(10):
    cap = cv2.VideoCapture(1)
    if cap.isOpened():
        print "opened"
        break
    else:
        print "camera didn't open"

clean_kernel = np.ones((5,5),np.uint8)

# define range of blue color in HSV
lower_blue = np.array([90,100,50])
upper_blue = np.array([115,255,255])

#define range of red color in HSV
lower_red = np.array([0,100,10])
upper_red = np.array([15,255,255])

# define range of green color in HSV
lower_green = np.array([55,80,10])
upper_green = np.array([90,255,255])


# return the largest contour's x and y position
def drawBoxes(binary_img,img,color,layer): # i don't actually know what the last arg is 
    contours,heirarchy = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return (-1,-1)
    contours = sorted(contours, key=lambda c:cv2.contourArea(c))
    biggestCnt = contours[-1]
    if (cv2.contourArea(biggestCnt) < 50): # probably just noise
        return (-1,-1)
    rx,ry,rw,rh = cv2.boundingRect(biggestCnt)
    cv2.rectangle(img,(rx,ry),(rx+rw,ry+rh),color,layer)
    return (rx,ry)

#######    TODO!!!     ########
def stopMotors():
    pass

def turnLeft():
    pass

def turnRight():
    pass

########  END TODO     #######

while(1):

    start = time.clock()
    
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get colors
    maskRed = cv2.inRange(hsv, lower_red, upper_red)
    maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)
    maskGreen = cv2.inRange(hsv, lower_green, upper_green)

    # process mask to clean noise
    cleanedRed = cv2.morphologyEx(maskRed, cv2.MORPH_OPEN, clean_kernel)
    cleanedBlue = cv2.morphologyEx(maskBlue, cv2.MORPH_OPEN, clean_kernel)
    cleanedGreen = cv2.morphologyEx(maskGreen, cv2.MORPH_OPEN, clean_kernel)

    # draw bounding boxes around different colors
    boxes = np.zeros(frame.shape,np.uint8)
    x,y = drawBoxes(cleanedRed,boxes,(0,0,255),1)
    if (x == -1) or (x > 300 and x < 340):
        stopMotors()
    elif (x <= 300):
        turnLeft()
    else:
        turnRight()

    elapsed = (time.clock() - start)

    #print elapsed
    
    cv2.imshow('frame',frame) # normal image
    cv2.imshow('cleaned red',cleanedRed)
    cv2.imshow('boxes',boxes)

    # end program when ESC is pressed
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
