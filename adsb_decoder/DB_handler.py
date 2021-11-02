from pymongo import MongoClient
import pyModeS as pms
import datetime
import math as Math
from bson.json_util import dumps
from pymongo.read_preferences import Primary
from .singletonDB import MongoConnectionSingleton
from numpy import arctan2,sin,cos,degrees

from .aircraftType import checkAircraftType

from .handler_aircraft_identity import create_new_aircraft_object
from .structureSurfacePosition import getSurfacePosStructure
from .structureAirborneVelocity import getAirborneVelocityStructure
from .structureAirbornePosition import getAirbornePosStructure
import time

class mongoDBClass:

    TIME_FORMAT = "%m/%d/%Y, %H:%M:%S" # month-data-year, hours-minutes-seconds
    # REF_LAT = 23.83588
    # REF_LON = 90.41611

    def __init__(self, lat, lng):
        self.REF_LAT = lat
        self.REF_LON = lng
        self.adsb_collection = MongoConnectionSingleton.get_instance()

        print('####################################### new mongoDb handler created[for debugging] #######################################')
        print("lat: ", self.REF_LAT)
        print("long: ", self.REF_LON)
        print()

    # cluster = MongoClient() #client = MongoClient('localhost', 27017)
    # # print(cluster)
    # db = cluster["planeInfo"]
    # adsb_collection = db['ADS-B']


    def createIdentityEntry(self, data, host):
        '''
        creates new entry for new icao address found
        
        '''
        aircraft = create_new_aircraft_object(data, host, self.TIME_FORMAT)
        self.adsb_collection.insert_one(aircraft)
        
    def handleID(self, data, host):
        '''
            if ICAO of msg doesn't exist in DB then a new entry is created for that ICAO
            data => [msg_icao, category, callsign, tc, msg]
            msg => [hexcodeMsg, timestamp]
        '''
        # msg_icao = pms.adsb.icao(msg)
        srch_res = self.adsb_collection.find_one({"icao":data[0]})
        if srch_res == None:
            self.createIdentityEntry(data, host)
        else:
            self.updateTimeStamp(data[0])

    def updateTimeStamp(self, icao): # complete this
        '''
            just updates the TimeStamp of the icao's data received
        '''
        # plane = adsb_collection.find_one({{"icao":icao}})

        pass



    def getAllData(self):
        '''
            returns all the data stored in the DB as an array of dictionary/JSON,
            meant to be used by server to send JSON data
        '''
        
        cursor = self.adsb_collection.find()
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        # for item in cursor:
        #     data.append(item)
        return json_data


    def getPlaneByIcao(self):
        pass
    
    def updateHexCodeAndTstamp(self, icao, hex, ts):
        '''
        updates timestamp and hexcode of a particular icao
        params=>(icao, hex, ts)
        
        '''
        # print("^^^^^^^^^^^^ GOT hex and ts ^^^^^^^^^^^^^^^^^^^^^^^^^")
        self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.signal.hexcode":hex}}) #data[4][0]==signal hsexcode
        self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.signal.timestamp":ts}}) #data[4][0]==signal timestamp
        

    def updateDecodedHex(self, icao, hex):
        '''
        params=>(icao, hex)
        
        \ndecode hex to:
        
        \n+----------+----------+-------------+------------------------+-----------+
        \n|  DF (5)  |  CA (3)  |  ICAO (24)  |         ME (56)        |  PI (24)  |
        \n+----------+----------+-------------+------------------------+-----------+

        '''
        hex2binData = pms.hex2bin(hex)

        df = pms.bin2int(hex2binData[0:5])
        ca = pms.bin2int(hex2binData[5:8])
        # me = pms.bin2int(hex2binData[32:88])
        me = hex[8:22]
        # tc = pms.bin2int(hex2binData[5:8])
        # parity = pms.bin2int(hex2binData[88:112])
        parity = hex[22:28]
        
        self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_hex.DF":df}}) #data[4][0]==signal hexcode
        self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_hex.CA":ca}}) #data[4][0]==signal hexcode
        self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_hex.ICAO":icao}}) #data[4][0]==signal hexcode
        self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_hex.ME":me}}) #data[4][0]==signal hsxcode
        self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_hex.PI":parity}}) #data[4][0]==signal hexcode
        # self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_hex.DF":hex}}) #data[4][0]==signal hexcode
        
        if pms.adsb.typecode(hex) in range(9,19) or range(20,23): #Airborne position
            structure = getAirbornePosStructure(hex)
            self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_msg.msg":{
                "TC":structure[0],
                "SS":structure[1],
                "SAF":structure[2],
                "ALT":structure[3],
                "T":structure[4],
                "F":structure[5],
                "LAT_CPR":structure[6],
                "LON_CPR":structure[7],
            }}}) 
            self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_msg.msg_type":"Airborne_position"}}) 
        
        elif pms.adsb.typecode(hex) in range(5,9): #Surface position
            structure = getSurfacePosStructure(hex)
            self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_msg.msg":{
                "TC":structure[0],
                "MOV":structure[1],
                "S":structure[2],
                "TRK":structure[3],
                "T":structure[4],
                "F":structure[5],
                "LAT_CPR":structure[6],
                "LON_CPR":structure[7],
            }}}) 
            self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_msg.msg_type":"Surface_position"}}) 
        
        elif pms.adsb.typecode(hex) == 19: #TC==19 so updates airborne velocity decoded message
            structure = getAirborneVelocityStructure(hex)
            # TC   |ST |IC|IFR|NUC|           |VrSrc|Svr|VR       |RESV|SDif|DAlt    
            self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_msg.msg":{
                "TC":structure[0],
                "ST":structure[1],
                "IC":structure[2],
                "IFR":structure[3],
                "NUC":structure[4],
                "WHAT":structure[5],
                "VrSrc":structure[6],
                "Svr":structure[7],
                "VR":structure[8],
                "RESV":structure[9],
                "SDir":structure[10],
                "SAlt":structure[11],
            }}}) 
            self.adsb_collection.update_one({"icao":icao}, {"$set":{"raw.decoded_msg.msg_type":"Airborne_velocity"}}) 
        

    # def updateRawDecodedMsg(self, msg):
    #     pass
    def updateAerealPos(self, data, host):
        '''
            \n updates areal position of an existing airplane in the DB
            \n data param receives a list => [icao, decoded_new_lat, decoded_new_long, alt,[hexcode,timestamp]]
            \n updates areal position of an existing airplane in the DB
            \n parms => (data, host); data=[icao, new_lat, new_long, altitude]
            \n data param receives a list => [icao, decoded_new_lat, decoded_new_long, alt]
        '''
        # lt, ln = pms.adsb.airborne_position_with_ref( msg, self.REF_LAT, self.REF_LON)
        # msg_icao = pms.adsb.icao(msg)
        
        # search_res = self.adsb_collection.find_one({"icao":data[0]})
        
        # print("$$$$$$ DATA $$$$$$$$$")
        # print(search_res)
        # print("$$$$$$ DATA $$$$$$$$")
        
        # if search_res != None and list(self.adsb_collection.find({"icao":data[0]},{"_id":0, "host":1}))[0]["host"]==host :
        if self.adsb_collection.find_one({"icao":data[0]}) != None and list(self.adsb_collection.find({"icao":data[0]}))[0]["host"]==host :
            # update data if icao entry already exists
            print('Update areal data ==========')
            search_res = self.adsb_collection.find_one({"icao":data[0]})
            current_Lat = search_res['flightInfo']['lat']
            current_Long = search_res['flightInfo']['long']
            
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.prevPos.what": current_Lat}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"inflight": True}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.lat": data[1]}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.long": data[2]}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.prevPos.lat": current_Lat}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.prevPos.long": current_Long}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.altitude":data[3]}}) #data[3]==altitude

            #the below code updates odd and even frames
            if pms.adsb.oe_flag(data[4][0]) == 0: # even frame
                self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.even_frame": [data[4][0], data[4][1]]  }}) #data[4][0]==signal hexcode, data[4][1]==signal timestamp
            elif pms.adsb.oe_flag(data[4][0]) == 1: # odd frame
                self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.odd_frame": [data[4][0], data[4][1]]  }}) #data[4][0]==signal hexcode, data[4][1]==signal timestamp
            
            # Globally unambigious position decoding starts here
            # if (self.adsb_collection.find({ "icao":data[0] })[0]["flightInfo"]["lat"] == None and self.adsb_collection.find({ "icao":data[0] })[0]["flightInfo"]["long"] == None) and self.adsb_collection.find({ "icao":data[0] })[0]["flightInfo"]["odd_frame"] != None and self.adsb_collection.find({ "icao":data[0] })[0]["flightInfo"]["even_frame"] != None:
            #     # an Icao's lat OR long doesn't exist AND the Icao's odd and even frame exists then calculate globally unambigious position
                
            #     odd = self.adsb_collection.find_one({"icao":data[0]})["flightInfo"]["odd_frame"]
            #     even = self.adsb_collection.find_one({"icao":data[0]})["flightInfo"]["even_frame"]
                
            #     pos = pms.adsb.position(even[0], odd[0], even[1], odd[1])
            #     #update position
            #     self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.lat": pos[0]}})
            #     self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.long": pos[1]}})

            #     #remove odd and even frames
            #     self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.even_frame": None  }}) # set even frame to None
            #     self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.odd_frame": None  }}) # set odd frame to None
            
            # elif self.adsb_collection.find({ "icao":data[0] })[0]["flightInfo"]["lat"] != None and  self.adsb_collection.find({ "icao":data[0] })[0]["flightInfo"]["long"] != None and pms.adsb.oe_flag(data[4][0]) == 0:
            #     # if  lat and long already exists then take that as reference point, the msg should also be even
            #     pos = pms.adsb.position_with_ref(data[4][0], self.adsb_collection.find_one({"icao":data[0]})["flightInfo"]["lat"], self.adsb_collection.find_one({"icao":data[0]})["flightInfo"]["long"])


            self.updateHexCodeAndTstamp(data[0], data[4][0], data[4][1]) #data[4][0]==signal hexcode, data[4][1]==signal timestamp
            self.updateDecodedHex(data[0], data[4][0])
            
            # self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"raw.signal.hexcode":data[4][0]}}) #data[4][0]==signal hsexcode
            # self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"raw.signal.timestamp":data[4][1]}}) #data[4][0]==signal timestamp
            
            if current_Lat != None:
                # calculate angle and make entry only if current_lat(ie previous lat now) exists
                newAngle = self.angleFromCoordinate(current_Lat, current_Long, data[1], data[2])
                self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.angle": int(newAngle)}})

            

        else:
            #do nothing if icao entry doesn't already exist
            pass

    def updateGndPos(self, data, host):
        '''
            \n updates GROUND position of an existing airplane in the DB
            \n data param receives a list => [icao, decoded_new_lat, decoded_new_long]
        '''

        # msg_icao = pms.adsb.icao(msg)
        # print(type(msg_icao))
        search_plane = self.adsb_collection.find_one({"icao": data[0]})
        print("search_plane: ", search_plane)
        if search_plane == None:
            print('plane does not exist for ground position update')
            pass # or should it be return

        elif search_plane['gndInfo']['lat'] ==None and search_plane['gndInfo']['long'] == None:
            # calculate initial position should implement globally ambigious position later
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"inGround": True}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"inflight": False}})
            
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"gndInfo.lat": data[1]}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"gndInfo.long": data[1]}})
            
        elif list(self.adsb_collection.find({"icao":data[0]},{"_id":0, "host":1}))[0]["host"]==host:
            # position already exists  should implement locally ambigious position later
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"inGround": True}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"inflight": False}})
            
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"gndInfo.lat": data[1]}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"gndInfo.long": data[0]}})
        
        self.updateHexCodeAndTstamp(data[0], data[3][0], data[3][1])  #data[3][0]==signal hexcode, data[3][0]==signal timestamp
        self.updateDecodedHex(data[0],data[3][0])
        

    # def updateAerealSpeed(self, icao, speed, host):
    #     pass



    # def updateGndSpeed(self, icao, lat, lng):
    #     pass

    def deleteByIcao(self, icao):
        pass


    def angleFromCoordinate(self, lat1,lon1,lat2,lon2) :
        '''
            returns angles in degress between two (lat,long) coordinates
            /n (old_lat, old_lon, new_lat, new_lon)
        '''
        # print("@@@@@@@@@#### calculate angle ######@@@@@@@@@@@")
        # print(lat1, lon1, lat2, lon2)
        # angle in degrees
        # angleDeg = Math.atan2(lon2 - lon1, lat2 - lat1) * 180 / Math.pi
        
        dL =Math.radians(lon2-lon1)
        lat1 = Math.radians(lat1)
        lat2 = Math.radians(lat2)
        lon1 = Math.radians(lon1)
        lon2 = Math.radians(lon2)
        X = cos(lat2)*sin(dL)
        Y = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dL)
        bearing = arctan2(X,Y)
        angleDeg = degrees(bearing)
        return angleDeg

    def handle_ArealVelocity(self, data, host):
        # handle gndVelocity here, gndVelocity is not done
        '''
        \nthe data praams receives a list [ icao, [speed, magHeading, verticalSpeed], [hexMsg, timestamp] ]

        \n
        Four different subtypes are defined in bits 6-8 of ME field. 
        With subtypes 1 and 2, ground speeds of aircraft are reported. 
        With subtypes 3 and 4, aircraft true airspeed or indicated 
        airspeed are included. Reporting of airspeed in ADS-B only 
        occurs when aircraft position can not be determined based on 
        the GNSS system.
        type:1,2 = Gnd Speed
        type:3,4 = True airspeed/indicated airspeed
        tupe:2,4 for supersonic aircraft, but they don't exist now, similat format to type 1,3
        '''
        # speed, magneticHeading, verticalSpeed , speedType = pms.adsb.velocity(msg)
        # ans = "speed: " + str(speed) + " " +"magHead: " + str(magneticHeading) + " " + "verticalSpeed: " + str(verticalSpeed) + " " + "speedType: " + str(speedType)
        

        if self.adsb_collection.find_one({"icao":data[0]}) != None and list(self.adsb_collection.find({"icao":data[0]},{"_id":0, "host":1}))[0]["host"]==host :
            
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.velocity.speed": data[1][0]}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.velocity.magHeading": data[1][1]}})
            self.adsb_collection.update_one({"icao":data[0]}, {"$set":{"flightInfo.velocity.verticalSpeed": data[1][2]}})
            self.updateHexCodeAndTstamp(data[0], data[2][0], data[2][1])
            self.updateDecodedHex(data[0], data[2][0])
            # self.updateRawDecodedMsg(data[0], data[2][0] )

    def handle_GndVelocity(self, msg,):
        '''
        Four different subtypes are defined in bits 6-8 of ME field. 
        With subtypes 1 and 2, ground speeds of aircraft are reported. 
        With subtypes 3 and 4, aircraft true airspeed or indicated 
        airspeed are included. Reporting of airspeed in ADS-B only 
        occurs when aircraft position can not be determined based on 
        the GNSS system.
        type:1,2 = Gnd Speed
        type:3,4 = True airspeed/indicated airspeed
        tupe:2,4 for supersonic aircraft, but they don't exist now, similat format to type 1,3
        '''
        pass

        

    def handle_data(self, msg):
        '''
            takes hexcode msaage, finds out type of data given and gives to approptiate data handler
        '''
        msgTC = pms.adsb.typecode(msg)

        if msgTC in range(9,19) or msgTC in range(20,23): #checking if TC == local aereal position
            self.updateAerealPos(msg) #msg structure => []

        elif msgTC in  range(1,5): #identity typecode
            self.handleID(msg)

        elif msgTC in range(5,9): #ground position
            self.updateGndPos(msg)

        elif msgTC == 19: #airborne velocity
            self.handle_ArealVelocity(msg)
            