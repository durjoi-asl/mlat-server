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

from TcpClient.readJson import readData

from csvHandler import csvWrite_rawHex
from tsDecoder import decodeTimeStampSeondsAndNanoSeconds
from posDecoder import getAdsbLatLon_fromRef
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

    def __init__(self,sensorInfo, dumpIcaoList,buffersize = 4096 ):
        '''
            params are: hostIP, portNumber, buffersize, lantLng(2D array containing the lat and long positions of the hostIP addresses ie gound station's LatLon position)
            eg for latLng = [[23.83588, 90.41611],[22.35443, 91.83391]]
        '''
        print(sensorInfo)

        self.sensorInfo = sensorInfo
        
        self.buffer = []
        self.buffersize = buffersize
        self.workerList = []

        self.dumpIcaoList = dumpIcaoList

        # self.latLng = latLng

        #initialize the DB connection
        

    def handleConnection(self, receiver, workerId):
        print('sensor: ',receiver)
        addr = (receiver["ip"], receiver["port"])
        
        # socket.connect(addr)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect(addr)

        # print("thread ID: ", workerId)
        # # print("latlng: ", la)
        # print("lat long: ", receiver["location"] )
        # # print("address: ", addr)
        # print("icaoList: ", self.dumpIcaoList)
        

        while True: 
            # print('sensor: ',receiver)
            print('sensor name: ',receiver['name'])
            print("in while loop, Worker ID: {}; Sensor Location".format(workerId, receiver['name']))

            # data = self.socket.recv(self.buffersize)
            data = sc.recv(self.buffersize)
            decoder = Decoder(data)
            # use a better way of using 
            decoder.handle_decode()
            messages_mlat = decoder.handle_messages()

            
            for msg in messages_mlat:
                # msg[0]=hexCode msg[1]=timeStamp

                df = pms.df(msg[0])
                

                # ADS-B - Mode S Long 28 byte
                if(df == 17):
                    icao = pms.adsb.icao(msg[0])

                    # thread_lat = receiver["location"][0]
                    # thread_lng = receiver["location"][1]

                    # msgHex = msg[0]
                    # msgTs = msg[1]

                    # print('msg; ', msg[1])

                    ts = decodeTimeStampSeondsAndNanoSeconds(msg[1])
                    # print('ts: ', ts[0], ts[1])
                    latLonFromRef = getAdsbLatLon_fromRef(msg[0], receiver['location'][0], receiver['location'][1])
                    if  latLonFromRef != False:
                        csvWrite_rawHex('raw/{0}/{1}.csv'.format(receiver['name'],icao), [ msg[0], msg[1], ts[0], ts[1], latLonFromRef[0][0], latLonFromRef[0][1], latLonFromRef[1] ])
                    


                     


    def handle_process(self):
        for workerId,receiver in enumerate(self.sensorInfo):
            
            self.workerList.append( multiprocessing.Process(target=self.handleConnection,args=(receiver,workerId,) ))
            
        
        
        for process in self.workerList:
            process.start()
            # process.join()


    


if __name__ == "__main__":
    sensorData = readData()
    print(sensorData)
    client = TcpClient(sensorData, ["iavl"])
    
    client.handle_process()
    print('worker list: ',client.workerList)