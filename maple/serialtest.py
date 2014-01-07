import serial
import time

ser = serial.Serial('/dev/tty.usbmodem1411', 115200)

def read():
    # print ser.read()
    pass

i = 0
dir = 1
while True:
    ser.write('S')
    read()
    ser.write(chr(i & 0xFF))
    read()
    ser.write(chr(i & 0xFF))
    read()
    ser.write('E')
    read()
    
    i += dir
    if i == 127:
        dir = -1

    if i == -127:
        dir = +1

    print i
    

    time.sleep(.1)

