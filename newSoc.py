import socket 
import threading 
from Decoder import Decoder
import pyModeS as pms
import decrypt
from jsonHandler import jsonHandlerClass
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


        while True: 
            print("in while loop, Thread ID: ", thread_id)
            
            data = self.socket.recv(self.buffersize) #receive data
            # print('[data]: ', data)
            print(f"\n[DATA PACKET] ------ {host} ----- {thread_id}")
            # print(format(data))
            # print("\n")
            decoder = Decoder(data)
            # decoder.handle_decode(data, self.latLng[thread_id-1][0], self.latLng[thread_id-1][1])
            decoder.handle_decode()
            messages_mlat = decoder.handle_messages()
            
            
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
                    
                       
                        
            

    # '''  for i, host_ip in enumerate(self.host): 
    #     newThread = threading.Thread(target=self.handle_connection, args=(host_ip, i+1))
        
    #     self.threadList.append(newThread)'''
    

    def run(self): 
        '''
        instantiates socket

        initiates handle_thread

        runs threads
        '''
        #creates the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #run the connection foreverrr
        self.handle_connection(self.host_ip, 0)

        

        # Starting all thread
        for thread in self.threadList:
            
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
            
# client = TcpClient(["192.168.30.27", "192.168.101.3"], 10003, [[23.83614, 90.41637],[22.35443, 91.83391]])
# client = TcpClient([ "192.168.30.27"], 10003, [[23.83614, 90.41637],[22.35443, 91.83391]]) #first receiver Perfecto
client = TcpClient([ "192.168.101.3"], 10003, [[22.35443, 91.83391]]) #second receiver perfecto
client.run()
