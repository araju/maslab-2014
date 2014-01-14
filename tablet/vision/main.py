# Handles the overall vision loop
# 1) Connect to camera
# 2) Read in frame
# 3) Resize frame and HSV thresh
# 4) Clean binary image and do blob detection
# 5) Process blob info
# 6) Publish list of balls with their distances and directions

import cv2
import process_frame as pf
import vis_publisher

def connectToCamera(videoIn):
    for i in range(10):
        cap = cv2.VideoCapture(videoIn)
        if cap.isOpened():
            print "opened"
            break
        else:
            print "camera didn't open"
            cap = None
    return cap

def main(videoIn):
    pub = VisPublisher(2300,12345)
    cap = connectToCamera(videoIn)
    while (1):
        _, frame = cap.read()
        blobs = pf.processFrame(frame) # blobs is a map of colors to lists of tuples (center, area)
        balls,reactors = processBlobs(blobs) # TODO implement this
        pub.publish(balls,reactors)
    pub.close()
    cv2.destroyAllWindows()
        
    

if __name__ == '__main__':
    videoIn = 1
    main(videoIn)
