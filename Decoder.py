class Decoder: 
    def __init__(self, buffer):
        super(Decoder, self).__init__()
        self.buffer = buffer
        # self.messages = []
        self.messages_mlat = []
        
    def handle_messages(self):
        # for msg in self.messages_mlat:
        #     # print(msg[1] + "   " + msg[0])
        #     # print(msg[1] in ALL_MESSAGES)
        #     # ALL_MESSAGES = [msg]
        #     return msg
        return self.messages_mlat
    
    def handle_decode(self):
        msg = []
        messages = []
        i = 0 

        while i < len(self.buffer):
            if self.buffer[i: i + 2] == [0x1A, 0x1A]:
                msg.append(0x1A)
                i += 1 
            elif (i == len(self.buffer) - 1) and (self.buffer[i] == 0x1A):
                # Special case where the last bit is 0x1A
                msg.append(0x1A)
            elif self.buffer[i] == 0x1A:
                if i == len(self.buffer) - 1:
                    # Special case where the last bit is 0x1A
                    msg.append(0x1A)
                elif len(msg) > 0:
                    messages.append(msg)
                    msg = []
            else: 
                msg.append(self.buffer[i])
            i += 1

        # Storing reminder for next reading cycle
        if len(msg) > 0:
            reminder = []
            for i, m in enumerate(msg):
                if (m == 0x1A) and (i < len(msg) - 1):
                    # rewind 0x1a, except when it is at the last bit
                    reminder.extend([m, m])
                else:
                    reminder.append(m)
            self.buffer = [0x1A] + msg
        else:
            self.buffer = []

        # Extracting Messages 
        self.messages_mlat = []

        for mm in messages: 
            msgtype = mm[0]
            msg = []
            
            if msgtype == 0x31: 
                # Mode-AC, 6 byte timestamp 1 byte signal level, 2 byte mode AC
                msg = "".join('%02X' % i for i in mm[8:])
                ts = "".join("%02X" % i for i in mm[1:8])
            elif msgtype == 0x32:
                # Mode-S short message, 6 byte timestamp 1 byte signal level, 7 byte Hex
                msg = "".join('%02X' % i for i in mm[8:])
                ts = "".join("%02X" % i for i in mm[1:8])
            elif msgtype == 0x33: 
                # Mode-S long message, 6 byte timestamp 1 byte signal level, 14 byte Hex
                msg = "".join('%02X' % i for i in mm[8:])
                ts = "".join("%02X" % i for i in mm[1:8])  
            else:
                # Other message type
                continue

            # if len(msg) not in [4, 14, 28]:
            #     continue
            
            if len(msg) not in [28, 14, 4]:
                continue
            
            self.messages_mlat.append([msg, ts])


