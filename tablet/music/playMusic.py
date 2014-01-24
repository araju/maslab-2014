from pygame import mixer

def play():
	mixer.init()
	mixer.music.load('Castle_of_Glass.mp3')
	mixer.music.play()
