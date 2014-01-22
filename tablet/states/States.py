# states.py
# list of states, mainly for use in main.py


IDLE = "IDLE"
EXPLORE = "EXPLORE"
GO_TO_BALL = "GO_TO_BALL"
GO_TO_REACTOR = "GO_TO_REACTOR"
WALL_FOLLOW = "WALL_FOLLOW"
RETURN_TO_WALL = "RETURN_TO_WALL"
DROP_RED = "DROP_RED"
SCORE = "SCORE"
STUCK = "STUCK"


stateActions = {
	IDLE : idle,
	EXPLORE : explore,
	GO_TO_BALL : goToBall,
	GO_TO_REACTOR : goToReactor,
	WALL_FOLLOW : wallFollow,
	RETURN_TO_WALL : retToWall,
	DROP_RED : dropRed,
	STUCK : stuck,
	SCORE : score
}

def getStateActions():
	return stateActions

def idle(sensors):
	pass # don't need to do anything in idle

def explore(sensors):
	print "unimplemented method: explore"

def goToBall(sensors):
	print "unimplemented method: goToBall"

def goToReactor(sensors):
	print "unimplemented method: goToReactor"

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