import socket 
import threading 
from Decoder import Decoder
import pyModeS as pms
# import decrypt
# from jsonHandler import jsonHandlerClass
import time
from DBmongoDB.DB_handler import mongoDBClass

from adsb_decoder.Decoder_V2 import PlaneInfoFactory
ADSB_MESSAGES = {}
DF_11 = {}
MODE_AC = {}

adsbd_AirCraftInfo = {}

# latLng = []

class TcpClient():
    '''
        constructor params are: hostIP, portNumber, buffersize, lantLng(2D array containing the lat and long positions of the hostIP addresses)
        \n eg for latLng = [[23.83588, 90.41611],[22.35443, 91.83391]]
    '''

    def __init__(self, host, port, latLng=[[23.83588, 90.41611],[22.35443, 91.83391]], buffersize = 4096):
        '''
            params are: hostIP, portNumber, buffersize, lantLng(2D array containing the lat and long positions of the hostIP addresses ie gound station's LatLon position)
            eg for latLng = [[23.83588, 90.41611],[22.35443, 91.83391]]
        '''

        super(TcpClient, self).__init__()
        
        self.host = host
        self.port = port
        self.buffer = []
        self.socket = None
        self.buffersize = buffersize
        self.threadList = []
        
        self.latLng = latLng

        #initialize the DB connection
        

    def handle_connection(self, host, thread_id):
        addr = (host, self.port)
        
        self.socket.connect(addr)
        
        #DB class instance
        # ADSB_db_handler = mongoDBClass(self.latLng[thread_id-1][0], self.latLng[thread_id-1][1])  

        print("thread ID: ", thread_id)
        # print("latlng: ", la)
        print("lat long: ",self.latLng[thread_id-1] )
        print("address: ", addr)
        print()
        

        while True: 
            print("in while loop, Thread ID: ", thread_id)
            
            # second method
            # print("DB lat: " ,ADSB_db_handler.REF_LAT)
            # print("DB long: " ,ADSB_db_handler.REF_LON)


            data = self.socket.recv(self.buffersize)
            # print('[data]: ', data)
            print(f"\n[DATA PACKET] ------ {host} ----- {thread_id}")
            # print(format(data))
            # print("\n")
            decoder = Decoder(data)
            # decoder.handle_decode(data, self.latLng[thread_id-1][0], self.latLng[thread_id-1][1])
            decoder.handle_decode()
            messages_mlat = decoder.handle_messages()
            

            # print("[messages_mlat] [2]: ", messages_mlat[2])
            # tempMsg = messages_mlat[1]
            # pms.tell(tempMsg[1])
            # print('temp: ', tempMsg)
            
            for msg in messages_mlat:
                # print('raw msg[0]: ', msg[0])
                df = pms.df(msg[0])
                

                # ADS-B - Mode S Long 28 byte
                if(df == 17):
                    icao = pms.adsb.icao(msg[0])

                    
                    thread_lat = self.latLng[thread_id-1][0]
                    thread_lng = self.latLng[thread_id-1][1]


                    PlaneInfoFactory.getInfoClass(msg[0], thread_lat, thread_lng, host)

                    if msg[0] in ADSB_MESSAGES.keys():
                        ADSB_MESSAGES[msg[0]][thread_id] = msg[1]
                        # print(f"{msg[0]} {ADSB_MESSAGES[msg[0]]}")
                        # print(ADSB_MESSAGES.keys())
                    else: 
                        ADSB_MESSAGES[msg[0]] = {}
                        ADSB_MESSAGES[msg[0]][thread_id] = msg[1]
                        ADSB_MESSAGES[msg[0]]["icao"] = icao
                        # print(f"{msg[0]} {ADSB_MESSAGES[msg[0]]}")
                    
                        
                        
                # All Call Reply - Mode S short 14 byte
                elif(df == 11):
                    icao = pms.adsb.icao(msg[0])
                    if icao in DF_11.keys():
                        DF_11[icao]["msg"] = msg[0]
                        DF_11[icao][str(thread_id)+"x"+str(DF_11[icao]["id"] + 1)] = msg[1]
                        DF_11[icao]["id"] = DF_11[icao]["id"] + 1
                        # print(f"{icao} {DF_11[icao]}")
                        # print(ALL_MESSAGES.keys())
                    else: 
                        DF_11[icao] = {}
                        DF_11[icao]["id"] = 0
                        DF_11[icao]["msg"] = msg[0]
                        DF_11[icao][str(thread_id)+"x"+str(DF_11[icao]["id"] + 1)] = msg[1]
                        DF_11[icao]["id"] = DF_11[icao]["id"] + 1
                        DF_11[icao]["icao"] = icao
                        # print(f"{icao} {DF_11[icao]}")
                       
                        
            
    def handle_thread(self):
        '''
        creates on thread for each receiver/groundStation then appends it to self.threadList
        '''
        
        for i, host_ip in enumerate(self.host): 
            newThread = threading.Thread(target=self.handle_connection, args=(host_ip, i+1))
            
            self.threadList.append(newThread)
    

    def run(self): 
        '''
        instantiates socket

        initiates handle_thread

        runs threads
        '''
        #creates the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Preparing thread
        self.handle_thread()

        # Starting all thread
        for thread in self.threadList:
            
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
            
# client = TcpClient(["192.168.30.27", "192.168.101.3"], 10003, [[23.83614, 90.41637],[22.35443, 91.83391]])
# client = TcpClient([ "192.168.30.27"], 10003, [[23.83614, 90.41637],[22.35443, 91.83391]]) #first receiver Perfecto
client = TcpClient([ "192.168.201.3"], 10003, [[22.82405, 89.55238]]) #third receiver perfecto
client.run()

#updated receiver 1 coordinates
# Latitude	23.83614° North
# Longitude	90.41637° East

# older coordinates
# [[23.83588, 90.41611],[22.35443, 91.83391]]