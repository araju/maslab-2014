import json
import sys
from PIL import Image, ImageDraw

#Assume that the map coordinates are in meters
#Assume that each pixel is 1cm x 1cm

SCALE_FACTOR = 100

def main(fName):
    mapPoints = ''
    with open(fName) as fileIn:
        mapPoints = json.load(fileIn)['map']

    maxX = 0
    maxY = 0

    for i in range(len(mapPoints)):

        mapPoints[i] = (mapPoints[i][0] * SCALE_FACTOR, \
                        mapPoints[i][1] * SCALE_FACTOR + 1)
        
        if mapPoints[i][0] > maxX:
            maxX = mapPoints[i][0]

        if mapPoints[i][1] > maxY:
            maxY = mapPoints[i][1]

    im = Image.new('RGB', (maxX, maxY), "white")
    imDraw = ImageDraw.Draw(im)

    for i in range(len(mapPoints)-1):
        imDraw.line([mapPoints[i], mapPoints[i+1]], fill = 'black')


    im.show()

if __name__ == '__main__':
    fName = 'map.json'
    if len(sys.argv) == 2:
        fName = sys.args[1]
    main(fName)