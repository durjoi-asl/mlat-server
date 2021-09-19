import socket 
import threading 
from Decoder import Decoder
import pyModeS as pms
import pandas as pd

ADSB_MESSAGES = {}
DF_11 = {}
MODE_AC = {}


class TcpClient():
    def __init__(self, host, port, buffersize = 4096):
        super(TcpClient, self).__init__()
        
        self.host = host
        self.port = port
        self.buffer = []
        self.socket = None
        self.buffersize = buffersize
        self.threadList = []
        self.dataFrame = None
        self.modes = None 
        self.modeac = None

    def handle_connection(self, host, thread_id):
        addr = (host, self.port)
        
        self.socket.connect(addr)
        self.dataFrame = pd.DataFrame()
        
        while True: 
            data = self.socket.recv(self.buffersize)
            print(f"\n[DATA PACKET] ------ {host} ----- {thread_id}")
            # print(format(data))
            # print("\n")
            decoder = Decoder(data)
            decoder.handle_decode()
            messages_mlat = decoder.handle_messages()
            
            for msg in messages_mlat:
               
                # ADS-B - Mode S Long 28 byte
                if len(msg[0]) == 4: 
                    # icao = pms.adsb.icao(msg[0])
                    
                    incomming_dataFrame = pd.DataFrame([[msg[0], msg[1], thread_id, host]], columns=['Message', 'Timestamp', 'Receiver', 'Receiver IP'])
                    if self.modeac is not None:
                        # self.dataFrame = self.dataFrame.append(incomming_dataFrame)
                        incomming_dataFrame.to_csv('modeac.csv', mode='a', header=None, index=False)  
                    else:
                        incomming_dataFrame.to_csv('modeac.csv', index=False)
                        self.modeac = incomming_dataFrame
                    incomming_dataFrame = None
                    # if msg[0] in MODE_AC.keys():
                    #     MODE_AC[msg[0]][thread_id] = msg[1]
                    #     print(f"{msg[0]} {MODE_AC[msg[0]]}")
                    #     # print(ALL_MESSAGES.keys())
                    # else: 
                    #     MODE_AC[msg[0]] = {}
                    #     MODE_AC[msg[0]][thread_id] = msg[1]
                    #     MODE_AC[msg[0]]["icao"] = icao
                    #     print(f"{msg[0]} {MODE_AC[msg[0]]}")
                else: 
                    df = pms.df(msg[0])
                    if df == 17:
                        
                        icao = pms.adsb.icao(msg[0])
                        
                        incomming_dataFrame = pd.DataFrame([[icao, msg[0], msg[1], thread_id, df, host]], columns=['Icao', 'Message', 'Timestamp', 'Receiver', 'df', 'Receiver IP'])
                        if self.dataFrame is not None:
                            # self.dataFrame = self.dataFrame.append(incomming_dataFrame)
                            incomming_dataFrame.to_csv('adsb.csv', mode='a', header=None, index=False)  
                        else:
                            incomming_dataFrame.to_csv('adsb.csv', index=False)
                            self.dataFrame = incomming_dataFrame
                            # self.dataFrame.to_csv('adsb.csv', header=True, index=False) 
                        incomming_dataFrame = None 
                        # if msg[0] in ADSB_MESSAGES.keys():
                        #     ADSB_MESSAGES[msg[0]][thread_id] = msg[1]
                        #     print(f"{msg[0]} {ADSB_MESSAGES[msg[0]]}")
                        #     # print(ALL_MESSAGES.keys())
                        # else: 
                        #     ADSB_MESSAGES[msg[0]] = {}
                        #     ADSB_MESSAGES[msg[0]][thread_id] = msg[1]
                        #     ADSB_MESSAGES[msg[0]]["icao"] = icao
                        #     print(f"{msg[0]} {ADSB_MESSAGES[msg[0]]}")
                        # print(self.dataFrame)
                        
                            
                    # All Call Reply - Mode S short 14 byte
                    elif df == 11:
                        icao = pms.adsb.icao(msg[0])
                        
                        incomming_dataFrame = pd.DataFrame([[icao, msg[0], msg[1], thread_id, df, host]], columns=['Icao', 'Message', 'Timestamp', 'Receiver', 'df', 'Receiver IP'])
                        if self.modes is not None:
                            # self.dataFrame = self.dataFrame.append(incomming_dataFrame)
                            incomming_dataFrame.to_csv('modes.csv', mode='a', header=None, index=False)  
                        else:
                            incomming_dataFrame.to_csv('modes.csv', index=False)
                            self.modes = incomming_dataFrame
                        incomming_dataFrame = None
                        # icao = pms.adsb.icao(msg[0])
                        # if icao in DF_11.keys():
                        #     DF_11[icao]["msg"] = msg[0]
                        #     DF_11[icao][str(thread_id)+"x"+str(DF_11[icao]["id"] + 1)] = msg[1]
                        #     DF_11[icao]["id"] = DF_11[icao]["id"] + 1
                        #     print(f"{icao} {DF_11[icao]}")
                        #     # print(ALL_MESSAGES.keys())
                        # else: 
                        #     DF_11[icao] = {}
                        #     DF_11[icao]["id"] = 0
                        #     DF_11[icao]["msg"] = msg[0]
                        #     DF_11[icao][str(thread_id)+"x"+str(DF_11[icao]["id"] + 1)] = msg[1]
                        #     DF_11[icao]["id"] = DF_11[icao]["id"] + 1
                        #     DF_11[icao]["icao"] = icao
                        #     print(f"{icao} {DF_11[icao]}")
                            
                            
                    # # Mode A/C - 4 byte
                    
            
    def handle_thread(self):
        
        for i, host_ip in enumerate(self.host): 
            newThread = threading.Thread(target=self.handle_connection, args=(host_ip, i+1))
            
            self.threadList.append(newThread)
    
    def run(self): 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Preparing thread
        self.handle_thread()

        # Starting all thread
        for thread in self.threadList:
            
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
            
client = TcpClient(["192.168.30.27", "192.168.101.3"], 10003)
client.run()