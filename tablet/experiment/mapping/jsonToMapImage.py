import json
import sys


def main(fName):
    mapPoints = ''
    with open(fName) as fileIn:
        mapPoints = json.load(fileIn)['map']
    print mapPoints
    for point in mapPoints:
        point[1] += 1

    print mapPoints

if __name__ == '__main__':
    fName = 'map.json'
    if len(sys.argv) == 2:
        fName = sys.args[1]
    main(fName)