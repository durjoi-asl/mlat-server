from pymongo import MongoClient
import pyModeS as pms
import datetime
import math as Math
from bson.json_util import dumps


class mongoDBClass:

    TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"
    # REF_LAT = 23.83588
    # REF_LON = 90.41611

    def __init__(self, lat, lng):
        self.REF_LAT = lat
        self.REF_LON = lng

        print('####################################### new mongoDb handler created[for debugging] #######################################')
        print("lat: ", self.REF_LAT)
        print("long: ", self.REF_LON)
        print()

    cluster = MongoClient() #client = MongoClient('localhost', 27017)
    # print(cluster)
    db = cluster["planeInfo"]
    adsb_collection = db['ADS-B']


    def createEntry(self, msg):
        '''
        creates new entry for new icao address found
        '''
        post = {
                "icao": pms.adsb.icao(msg),
                "identity":{
                    "category":pms.adsb.category(msg),
                    "callsign":pms.adsb.callsign(msg)
                    },
                "inflight": False,
                "inGround": False,
                "flightInfo": {
                    "lat":None,
                    "long": None,
                    "velocity": {
                        "speed": None,
                        "magHeading": None,
                        "verticalSpeed": None
                    },
                    "altitude": None,
                    "prevPos": {
                        "lat": None,
                        "long": None
                    },
                    "angle": 0

                },
                "gndInfo": {
                    "lat": None,
                    "long": None,
                    "speed": None,
                    "altitude" :None
                },
                "last_updated": datetime.datetime.now().strftime(self.TIME_FORMAT)
            }

        self.adsb_collection.insert_one(post)
        

    def getAllData(self):
        '''
            returns all the data stored in the DB as an array of dictionary/JSON,
            meanto to be used by server to send JSON data
        '''
        
        cursor = self.adsb_collection.find()
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        # for item in cursor:
        #     data.append(item)
        return json_data

    def getPlaneByIcao(self):
        pass

    def updateAerealPos(self, msg):
        '''
            updates areal position of an existing airplane in the DB
        '''
        lt, ln = pms.adsb.airborne_position_with_ref( msg, self.REF_LAT, self.REF_LON)
        msg_icao = pms.adsb.icao(msg)
        search_res = self.adsb_collection.find_one({"icao":msg_icao})
        if search_res != None:
            # update data if icao entry already exists
            print('Update areal data ==========')
            
            current_Lat = search_res['flightInfo']['lat']
            current_Long = search_res['flightInfo']['long']

            #UPDATE flight lat, long, inflight status, previousePos.lat and previousePos.long
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"inflight": True}})
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.lat": lt}})
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.long": ln}})
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.prevPos.lat": current_Lat}})
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.prevPos.long": current_Long}})

            if current_Lat != None:
                # calculate angle and make entry only if current_lat(ie previous lat now) exists
                newAngle = self.angleFromCoordinate(current_Lat, current_Long, lt, ln)
                self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.angle": newAngle}})

        else:
            #do nothing if icao entry doesn't already exist
            pass

    def updateGndPos(self, msg):
        msg_icao = pms.adsb.icao(msg)
        print(type(msg_icao))
        search_plane = self.adsb_collection.find_one({"icao": msg_icao})
        print("search_plane: ", search_plane)
        if search_plane == None:
            print('================================== ground position ==================================')
            print('plane does not exist for ground position update')
            print('icao: '+msg_icao)
            lt, ln = pms.adsb.position_with_ref(msg, self.REF_LAT, self.REF_LON)
            print('lat: ', lt)
            print('long: ', ln)
            pass
        elif search_plane['gndInfo']['lat'] ==None and search_plane['gndInfo']['long'] == None:
            # calculate initial position should implement globally ambigious position later
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"inGround": True}})
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"inflight": True}})
            lt, ln = pms.adsb.position_with_ref(msg, self.REF_LAT, self.REF_LON)
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"gndInfo.lat": lt}})
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"gndInfo.long": ln}})
        else:
            # position already exists  should implement locally ambigious position later
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"inGround": True}})
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"inflight": True}})
            lt, ln = pms.adsb.position_with_ref(msg, self.REF_LAT, self.REF_LON)
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"gndInfo.lat": lt}})
            self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"gndInfo.long": ln}})
        pass

    def updateAerealSpeed(self, icao, speed):
        pass



    def updateGndSpeed(self, icao, lat, lng):
        pass

    def deleteByIcao(self, icao):
        pass

    def handleID(self, msg):
        msg_icao = pms.adsb.icao(msg)
        srch_res = self.adsb_collection.find_one({"icao":msg_icao})
        if srch_res == None:
            self.createEntry(msg)
        else:
            self.updateTimeStamp(msg_icao)

    def updateTimeStamp(self, icao):
        '''
            just updates the TimeStamp of the icao's data received
        '''
        # plane = adsb_collection.find_one({{"icao":icao}})

        pass


    def angleFromCoordinate(self, lat1,lon1,lat2,lon2) :
        '''
            returns angles in degress between to (lat,long) coordinates
            /n (old_lat, old_lon, new_lat, new_lon)
        '''
        # angle in degrees
        angleDeg = Math.atan2(lon2 - lon1, lat2 - lat1) * 180 / Math.pi
        return angleDeg

    def handle_ArealVelocity(self, msg):
        # handle gndVelocity here, gndVelocity is not done
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
        # speed, magneticHeading, verticalSpeed , speedType = pms.adsb.velocity(msg)
        # ans = "speed: " + str(speed) + " " +"magHead: " + str(magneticHeading) + " " + "verticalSpeed: " + str(verticalSpeed) + " " + "speedType: " + str(speedType)
        try :
            data = pms.adsb.velocity(msg)
            print(data)
            msg_icao = pms.adsb.icao(msg)
            if self.adsb_collection.find_one({"icao":msg_icao}) != None:
                # update air speed
                # pass
                self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.velocity.speed": data[0]}})
                self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.velocity.magHeading": data[1]}})
                self.adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.velocity.verticalSpeed": data[2]}})
                
        except :
            # figure out why error arises sometimes
            print('error air speed, icao: ', msg_icao)

    def handle_GndVelocity(self, msg):
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

        

    def handle_data(self, msg):
        msgTC = pms.adsb.typecode(msg)
        if msgTC in range(9,19) or msgTC in range(20,23): #checking if TC == local aereal position
            print('not updataing yet...')
            self.updateAerealPos(msg)
        elif msgTC in  range(1,5): #identity typecode
            self.handleID(msg)
        elif msgTC in range(5,9): #ground position
            
            # self.updateGndPos(msg)
            print('================================== ground position ==================================')
            # print(' ')
        elif msgTC == 19: #airborne velocity
            self.handle_ArealVelocity(msg)
            