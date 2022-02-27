from operator import indexOf
import sys 
sys.path.append("..")

import socket 
import threading 
from Decoder import Decoder
import pyModeS as pms

import time
from DBmongoDB.DB_handler import mongoDBClass

import multiprocessing

from adsb_decoder.Decoder_V2 import PlaneInfoFactory

from readJson import readData



import json

ADSB_MESSAGES = {}
DF_11 = {}
MODE_AC = {}

adsbd_AirCraftInfo = {}


class TcpClient():
    '''
        constructor params are: hostIP, portNumber, buffersize, lantLng(2D array containing the lat and long positions of the hostIP addresses)
        \n eg for latLng = [[23.83588, 90.41611],[22.35443, 91.83391]]
    '''

    def __init__(self,sensorInfo, buffersize = 4096):
        '''
            params are: hostIP, portNumber, buffersize, lantLng(2D array containing the lat and long positions of the hostIP addresses ie gound station's LatLon position)
            eg for latLng = [[23.83588, 90.41611],[22.35443, 91.83391]]
        '''

        self.sensorInfo = sensorInfo
        
        self.buffer = []
        self.buffersize = buffersize
        self.workerList = []

        
        # self.latLng = latLng

        #initialize the DB connection
        

    def handleConnection(self, receiver, workerId):

        addr = (receiver["ip"], receiver["port"])
        
        # socket.connect(addr)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect(addr)

        print("thread ID: ", workerId)
        # print("latlng: ", la)
        print("lat long: ", receiver["location"] )
        # print("address: ", addr)
        print()
        

        while True: 
            print("in while loop, Worker ID: ", workerId)
            print(receiver["name"])

            # data = self.socket.recv(self.buffersize)
            data = sc.recv(self.buffersize)
            decoder = Decoder(data)
            # use a better way of using 
            decoder.handle_decode()
            messages_mlat = decoder.handle_messages()

            
            for msg in messages_mlat:
                print('raw msg[0]: ', msg[0])
                print('raw message: ', msg)
                df = pms.df(msg[0])
                

                # ADS-B - Mode S Long 28 byte
                if(df == 17):
                    icao = pms.adsb.icao(msg[0])

                    
                    thread_lat = receiver["location"][0]
                    thread_lng = receiver["location"][1]

                    #msg[0] = msg
                    #msg[1] = timestamp
                    #msg = [hex_msg, timestamp]
                    #was sending msg[0], now refactoring and sending the whole msg
                    PlaneInfoFactory.getInfoClass(msg, thread_lat, thread_lng, receiver["ip"])

                    if msg[0] in ADSB_MESSAGES.keys():
                        ADSB_MESSAGES[msg[0]][workerId] = msg[1]
                        # print(f"{msg[0]} {ADSB_MESSAGES[msg[0]]}")
                        # print(ADSB_MESSAGES.keys())
                    else: 
                        ADSB_MESSAGES[msg[0]] = {}
                        ADSB_MESSAGES[msg[0]][workerId] = msg[1]
                        ADSB_MESSAGES[msg[0]]["icao"] = icao
                        # print(f"{msg[0]} {ADSB_MESSAGES[msg[0]]}")
                    
                        
                        
                # All Call Reply - Mode S short 14 byte
                # if(df == 11):
                #     icao = pms.adsb.icao(msg[0])
                #     if icao in DF_11.keys():
                #         DF_11[icao]["msg"] = msg[0]
                #         DF_11[icao][str(workerId)+"x"+str(DF_11[icao]["id"] + 1)] = msg[1]
                #         DF_11[icao]["id"] = DF_11[icao]["id"] + 1
                #         # print(f"{icao} {DF_11[icao]}")
                #         # print(ALL_MESSAGES.keys())
                #     else: 
                #         DF_11[icao] = {}
                #         DF_11[icao]["id"] = 0
                #         DF_11[icao]["msg"] = msg[0]
                #         DF_11[icao][str(workerId)+"x"+str(DF_11[icao]["id"] + 1)] = msg[1]
                #         DF_11[icao]["id"] = DF_11[icao]["id"] + 1
                #         DF_11[icao]["icao"] = icao
                        # print(f"{icao} {DF_11[icao]}")
                       


    def handle_process(self):
        for workerId,receiver in enumerate(self.sensorInfo):
            
            self.workerList.append( multiprocessing.Process(target=self.handleConnection,args=(receiver,workerId,) ))
            
        
        
        for process in self.workerList:
            print("indexOf(process)", self.workerList.index(process))
            process.start()
            # process.join()


    


if __name__ == "__main__":
    data = readData()
    client = TcpClient(data)
    
    client.handle_process()
    # print(client.workerList)