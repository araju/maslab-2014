# states.py
# list of states, mainly for use in main.py


IDLE = "IDLE"
EXPLORE = "EXPLORE"
GO_TO_OBJ = "GO_TO_OBJ"
WALL_FOLLOW = "WALL_FOLLOW"
RETURN_TO_WALL = "RETURN_TO_WALL"
DROP_RED = "DROP_RED"
SCORE = "SCORE"
STUCK = "STUCK"


stateActions = {
	IDLE : idle,
	EXPLORE : explore,
	GO_TO_OBJ : goToObj,
	WALL_FOLLOW : wallFollow,
	RETURN_TO_WALL : retToWall,
	DROP_RED : dropRed,
	STUCK : stuck,
	SCORE : score
}

def getStateActions():
	return stateActions

def idle(sensors):
	print "unimplemented method: idle"

def explore(sensors):
	print "unimplemented method: explore"

def goToObj(sensors):
	print "unimplemented method: goToObj"

def wallFollow(sensors):
	print "unimplemented method: wallFollow"

def retToWall(sensors):
	print "unimplemented method: retToWall"

def dropRed(sensors):
	print "unimplemented method: dropRed"

def stuck(sensors):
	print "unimplemented method: stuck"

def score(sensors):
	print "unimplemented method: score"