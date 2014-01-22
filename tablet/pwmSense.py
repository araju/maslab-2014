class PWMSense:
    def __init__ (self, maple):
        self.maple = maple
        self.pwmChannels = [0,0]

        def pwmCb(arg_list):
            motor = int(arg_list[1]) & 0x01
            sign = 1
            sign += -2 * ((int(arg_list[1]) & 0x80) >> 7)

            mag = int(arg_list[2]) | (int(arg_list[3]) << 8)

            self.pwmChannels[motor] = sign * mag

        self.maple.registerCb(0x17, pwmCb)