# botclient_comm.py
# Communicates with the BotClient Server

# TODO: look at java client to double check if we are doing it right


class BotClientCommunicator:

	def __init__(self, host, port):
		print "unimplemented class: BotClientCommunicator"
		self.recvStartSignal = False
		self.recvStopSignal = False

		self.svrSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.svrSock.bind((host port))
		self.svrSock.listen(5)
		thread = Thread(target = self.startServer)
		thread.start()

	# TODO: test this shit!! can it get multiple messages from same connection?
	def startServer(self):
		while True:
			clisock, (remhost, remport) = srvsock.accept()
	  		msg = clisock.recv(4096)
	  		if (msg.startswith("start")):
	  			self.recvStartSignal = True
	  		elif (msg.startswith("stop")):
	  			self.recvStopSignal = True
	  		else:
	  			pass # maybe it's the map, or some json. w/e. deal with it later maybe
	  		



