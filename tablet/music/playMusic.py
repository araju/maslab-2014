from pygame import mixer

def play():
	mixer.init()
	mixer.music.load('music/Castle_of_Glass.mp3')
	mixer.music.play()
	print "playing!"
