
import sys
import serial
import serial.tools
import serial.tools.list_ports
import traceback
import time


class Maple:
    ESCAPE = 0x7F
    START_FLAG = 0x55
    END_FLAG = 0xAA

    # ESCAPE = '!'
    # START_FLAG = 'A'
    # END_FLAG = 'Z'

    def __init__(self):
        self.portName = self._findMaplePort()
        self.port = serial.Serial(port=self.portName, timeout = 0, \
                                  writeTimeout = 0)
        self.cbList = {}
        self.inCommand = False
        self.isEscaped = False
        self.buffer = []

    def _findMaplePort(self):
        for port in serial.tools.list_ports.comports():
            if port[1].startswith('Maple'):
                return port[0]

    def periodic_task(self):
        printCr = False
        while self.port.inWaiting():
            printCr = True
            ch = ord(self.port.read())
            print chr(ch),
            if self.isEscaped:
                self.isEscaped = False
                self.buffer.append(ch)
            else:
                if ch == self.START_FLAG:
                    self.buffer = []
                elif ch == self.END_FLAG:
                    #process message
                    if self._validMessage():
                        #if this is a valid message, the first entry will be 
                        # the key for a call back function.  We call the
                        #callback function with the arguments for that command.
                        cb = self.cbList[self.buffer[0]]
                        cb(self.buffer[1:-1])
                elif ch == self.ESCAPE:
                    self.isEscaped = True
                else:

                    self.buffer.append(ch)

        if printCr:
            print ''
    def _validMessage(self):
        checksum = 0
        for ch in self.buffer:
            checksum += ch

        return checksum & 0xFF == 0xFF


    def close(self):
        self.port.close()

    def registerCb(self,command, callback):
        if command in self.cbList.keys():
            raise Exception('Callback already allocated')
        self.cbList[command] = callback

    def send(self,bytes):
        #The message format is:
        #Start Flag
        #command
        #arglength
        #args
        #checksum
        #endflag
        checksum = 0
        outBytes = bytearray()
        outBytes.append(self.START_FLAG)
        for b in bytes:
            if b in [self.START_FLAG, self.END_FLAG, self.ESCAPE]:
                outBytes.append(b)
            outBytes.append(b)
            checksum += b
        outBytes.append((~checksum) & 0xFF)
        outBytes.append(self.END_FLAG)

        print 'Sending: ',
        for i in outBytes:
            print hex(i), 
        print ''
        self.port.write(outBytes)
def periodic_hook():
    pass


    

def main():
    maple = Maple()

    def testCb(args):
        print 'Received: ', args
        length = args[0]
        num = args[1] | (args[2] << 8)
        num += 1
        buf = [0x00,0x02,num & 0xFF, (num >> 8) & 0xFF]
        maple.send(buf)

    maple.registerCb(0x00, testCb)
    try:
        run = True
        # maple.open()
        print 'Port is Open'
        # maple.send([0x00, 0x02, 0x00, 0x00])
        while run:
            time.sleep(1)
            maple.periodic_task()
            
    except:
        traceback.print_exc()
        if maple != None:
            maple.close()

if __name__ == '__main__':
    main()