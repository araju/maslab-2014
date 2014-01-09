
import sys
import serial
import serial.tools
import serial.tools.list_ports

def findMaplePort():
	for port in serial.tools.list_ports.comports():
		if port[1].startswith('Maple'):
			return port[0]

	return None

def main():
	#find open ports
	port = findMaplePort()
	if port is None:
		sys.exit('Can\'t find maple port!')

	print port

if __name__ == '__main__':
	main()