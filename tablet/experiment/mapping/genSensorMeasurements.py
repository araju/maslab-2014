import json
import math
import sys
import random

def importJsonFile(fName):
    mapPoints = ''
    with open(fName) as fileIn:
        mapPoints = json.load(fileIn)

    return mapPoints

def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** .5

def generateSensorMeasurements(mapPoints, position, noiseLevel = 0):
    ret = {}

    walls = [(mapPoints[i], mapPoints[i+1]) for i in range(len(mapPoints)-1)]


    distToWalls = []
    for i in range(4):

        endpoint = \
                (10 * math.cos(math.radians(i * 90 + position[2])) + position[0], \
                10 * math.sin(math.radians(i * 90 + position[2])) + position[1])

        for wall in walls:
            intersection = findIntersection((position, endpoint), wall)
            if intersection is not None:
                distToWalls.append(distance(position,intersection) + \
                    random.gauss(0, noiseLevel))
                break

    return distToWalls

            



def findIntersection(line1, line2):

    # In order for an intersection to happen between two line segments the
    # following conditions need to be true:
    #  - They must share a range of x values
    #  - After checking the y locations at the start and end of the shared 
    #      X range, they must swap positions.

    left1 = line1[0]
    right1 = line1[1]
    if left1[0] > right1[0]:
        left1, right1 = right1, left1

    left2 = line2[0]
    right2 = line2[1]
    if left2[0] > right2[0]:
        left2, right2 = right2, left2

    #Check to see if there is a shared range
    if right2[0] < left1[0] or left2[0] > right1[0]:
        # the X range isn't share
        return None

    # Find the shared range 
    sharedLeftX = left1[0]
    if left1[0] <= left2[0]:
        sharedLeftX = left2[0]

    sharedRightX = right1[0]
    if right1[0] >= right2[0]:
        sharedRightX = right2[0]

    try:
        slope1 = None
        slope2 = None

        eps = 0

        slope1 = (right1[1] - left1[1]) / (right1[0] - left1[0] + eps)

        # This is added because the inexactness of floating point numbers
        # If the slope is too steep, assume that it is actually vertical
        if (abs(slope1) > 1e3):
            slope1 = None
            raise Exception()
        
        yint1 = left1[1] - slope1 * left1[0]


        slope2 = (right2[1] - left2[1]) / (right2[0] - left2[0] + eps)

        if (abs(slope2) > 1e3):
            slope2 = None
            raise Exception()

        yint2 = left2[1] - slope2 * left2[0]

        # Check the start and end y values
        sharedLeftY1 = slope1 * sharedLeftX + yint1
        sharedLeftY2 = slope2 * sharedLeftX + yint2

        sharedRightY1 = slope1 * sharedRightX + yint1
        sharedRightY2 = slope2 * sharedRightX + yint2


        # This checks to see if there was a swap ie. at the start of the shared
        # range, one light is above the other and at the end of the range that
        # line is now below the other line
        if not ((sharedLeftY1 > sharedLeftY2) ^ (sharedRightY1 > sharedRightY2)):
            return None

        xCross = (yint2 - yint1) / (slope1 - slope2)
        yCross = slope1 * xCross + yint1

        return (xCross, yCross)

    except:
        # We're here because we tried to divide by zero when calculating the slope
        # Let's find which one is vertical
        if slope1 is None:
            # line 1 is vertical
            xCross = right1[0]

            slope2 = (right2[1] - left2[1]) / (right2[0] - left2[0])
            yint2 = left2[1] - slope2 * left2[0]

            yCross = slope2 * xCross + yint2

            
        elif slope2 is None:
            # line 2 is vertical
            xCross = right2[0]

            yCross = slope1 * xCross + yint1

        return xCross, yCross
        

def main(fName):

    mapPoints = importJsonFile(fName)

    track = mapPoints['movement']
    points = mapPoints['map']
    mapPoints['measurements'] = []
    noiseLevel = .25
    for point in track:
        mapPoints['measurements'].append( \
            generateSensorMeasurements(points, point, noiseLevel = .25))
        
    with open(fName, 'w') as fileOut:
            json.dump(mapPoints, fileOut, indent=4)
    
if __name__ == '__main__':
    fName = 'map.json'
    if len(sys.argv) == 2:
        fName = sys.args[1]
    main(fName)