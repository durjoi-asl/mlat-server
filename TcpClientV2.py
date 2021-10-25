'''
insdead of multiProcessing we'll be creating new instances for each ground station
'''
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

class GroundStation():
    '''
    class for ground station, handles all information that the groundStation receives

    params of constructor: host IP, station number, portNo
    '''

    def __init__(self, host, stationNumber, portNo, ref_latLng, buffersize = 4096): #ref_latLng=[[23.83588, 90.41611],[22.35443, 91.83391]]
        self.host = host
        self.stationNumber = stationNumber
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = portNo
        self.latLng = ref_latLng
        self.buffersize = buffersize
    
    def handle_connection(self, host): # param: thread_id=self.stationNumber
        '''
            handles all data coming from ground station decodes and handles the decoded data
            params: host-IP, groundStation_number/ thread_id, ref_lat
        '''
        addr = (host, self.port)
        thread_id = self.stationNumber
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

                    
                    thread_lat = self.latLng[0]
                    thread_lng = self.latLng[1]


                    PlaneInfoFactory.getInfoClass(msg[0], thread_lat, thread_lng)


                    # PRACTICING ERROR CODE HANDLING
                    # try:
                    #     print("nuc_p ERROR=======   ",pms.adsb.nuc_p(msg[0]))
                    #     print("nuc_v ERROR=======   ",pms.adsb.nuc_v(msg[0]))
                    #     print("Version ERROR=======   ",pms.adsb.version(msg[0]))
                    # except:
                    #     print("ooy teri")
                    # remove from production code

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
                       
                        
                # # Mode A/C - 4 byte
                # else: 
                #     if msg[0] in MODE_AC.keys():
                #         MODE_AC[msg[0]][thread_id] = msg[1]
                #         print(f"{msg[0]} {MODE_AC[msg[0]]}")
                #         # print(ALL_MESSAGES.keys())
                #     else: 
                #         MODE_AC[msg[0]] = {}
                #         MODE_AC[msg[0]][thread_id] = msg[1]
                #         MODE_AC[msg[0]]["icao"] = icao
                #         print(f"{msg[0]} {MODE_AC[msg[0]]}")
            # time.sleep(3) 
    
    def runStation(self):
        print('groundStation Started: ', self.stationNumber)
        '''
            calls the handle_connection for groundStation object created, no params
        '''
        self.handle_connection(self.host)

    def printStation(self):
        print()
        print("##### ground station #####")
        print("host: ", self.host)
        print("stationNumber: ", self.stationNumber)
        print("port: ", self.port)
        print("ref_latLng: ", self.latLng)
        print("buffersize: ", self.buffersize)
        print()

class TcpClient():
    '''
        constructor params are: hostIP, portNumber, buffersize, lantLng(2D array containing the lat and long positions of the hostIP addresses)
        \n eg for latLng = [[23.83588, 90.41611],[22.35443, 91.83391]]
    '''

    def __init__(self, host, port, latLng=[[23.83588, 90.41611],[22.35443, 91.83391]], buffersize = 4096):
        '''
            params are: hostIP, portNumber, buffersize, lantLng(2D array containing the lat and long positions of the hostIP addresses)
            eg for latLng = [[23.83588, 90.41611],[22.35443, 91.83391]]
        '''

        super(TcpClient, self).__init__()
        
        self.host = host
        self.port = port
        self.buffer = []
        self.socket = None
        self.buffersize = buffersize
        self.threadList = []

        #NEW way of doing things
        self.groundStations = []
        
        self.latLng = latLng

        #initialize the DB connection
        

    def handle_connection(self, host, thread_id):
        '''
        creates socket to connect with signal receiver to decode data and send it to DB handler
        runs in infinite while loop

        '''
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


                    PlaneInfoFactory.getInfoClass(msg[0], thread_lat, thread_lng)


                    # PRACTICING ERROR CODE HANDLING
                    # try:
                    #     print("nuc_p ERROR=======   ",pms.adsb.nuc_p(msg[0]))
                    #     print("nuc_v ERROR=======   ",pms.adsb.nuc_v(msg[0]))
                    #     print("Version ERROR=======   ",pms.adsb.version(msg[0]))
                    # except:
                    #     print("something unexpected happened, ERROR")
                    # remove from production code

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
                       
                        
                # # Mode A/C - 4 byte
                # else: 
                #     if msg[0] in MODE_AC.keys():
                #         MODE_AC[msg[0]][thread_id] = msg[1]
                #         print(f"{msg[0]} {MODE_AC[msg[0]]}")
                #         # print(ALL_MESSAGES.keys())
                #     else: 
                #         MODE_AC[msg[0]] = {}
                #         MODE_AC[msg[0]][thread_id] = msg[1]
                #         MODE_AC[msg[0]]["icao"] = icao
                #         print(f"{msg[0]} {MODE_AC[msg[0]]}")
            # time.sleep(3) 
            
    def handle_thread(self):
        
        # for i, host_ip in enumerate(self.host): 
        #     newThread = threading.Thread(target=self.handle_connection, args=(host_ip, i+1))
            
        #     self.threadList.append(newThread)
        for station in self.groundStations:
            newThread = threading.Thread(target=station.runStation)
            self.threadList.append(newThread)
    
    def handle_groundStations(self):
        '''
        creates groundStation object for each receiver/groundStation and appends it to self.groundStations list
        '''
        for indx, host_ip in enumerate(self.host): 
            # newThread = threading.Thread(target=self.handle_connection, args=(host_ip, i+1))
            newStation = GroundStation(host_ip, indx+1, self.port, ref_latLng=self.latLng[indx])
            
            # self.threadList.append(newThread)
            self.groundStations.append(newStation)
    
    def run(self): 
        #creates the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



        # initiate ground stations
        self.handle_groundStations()

        # Preparing thread
        self.handle_thread()

        # Starting all threads
        for thread in self.threadList:
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

        #initiate all ground Stations
        print("groundStationList Len: ", len(self.groundStations))
        print("groundStationList : ", self.groundStations)
        for groundStation in self.groundStations:
            # groundStation.runStation()
            groundStation.printStation()
            groundStation.runStation()
            
client = TcpClient(["192.168.30.27", "192.168.101.3"], 10003, [[23.83614, 90.41637],[22.35443, 91.83391]])
# client = TcpClient([ "192.168.30.27"], 10003, [[23.83614, 90.41637],[22.35443, 91.83391]]) #first receiver Perfecto
# client = TcpClient([ "192.168.101.3"], 10003, [[22.35443, 91.83391]]) #second receiver perfecto
client.run()

#updated receiver 1 coordinates
# Latitude	23.83614° North
# Longitude	90.41637° East

# older coordinates
# [[23.83588, 90.41611],[22.35443, 91.83391]]