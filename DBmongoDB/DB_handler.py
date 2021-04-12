from pymongo import MongoClient
import pyModeS as pms
import datetime
import math as Math


# flass mongoDBClass:

TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"
REF_LAT = 23.83588
REF_LON = 90.41611

cluster = MongoClient() #client = MongoClient('localhost', 27017)
# print(cluster)
db = cluster["planeInfo"]
adsb_collection = db['ADS-B']


def createEntry(msg):
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
                "speed": None,
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
            "last_updated": datetime.datetime.now().strftime(TIME_FORMAT)
        }

    adsb_collection.insert_one(post)
    

def getAllData():
    '''
        returns all the data stored in the DB as an array of dictionary/JSON
    '''
    data = []
    cursor = adsb_collection.find()
    for item in cursor:
        data.append(item)
    return data

def getPlaneByIcao():
    pass

def updateAerealPos(msg):

    lt, ln = pms.adsb.airborne_position_with_ref( msg, REF_LAT, REF_LON)
    msg_icao = pms.adsb.icao(msg)
    search_res = adsb_collection.find_one({"icao":msg_icao})
    if search_res != None:
        #update data if icao entry already exists
        print('updating Stuff==========')
        
        current_Lat = search_res['flightInfo']['lat']
        current_Long = search_res['flightInfo']['long']

        #UPDATE flight lat, long, inflight status, previousePos.lat and previousePos.long
        adsb_collection.update_one({"icao":msg_icao}, {"$set":{"inflight": True}})
        adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.lat": lt}})
        adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.long": ln}})
        adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.prevPos.lat": current_Lat}})
        adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.prevPos.long": current_Long}})

        if current_Lat != None:
            # calculate angle and make entry only if current_lat(ie previous lat now) exists
            newAngle = angleFromCoordinate(current_Lat, current_Long, lt, ln)
            adsb_collection.update_one({"icao":msg_icao}, {"$set":{"flightInfo.angle": newAngle}})

    else:
        #do nothing if icao entry doesn't already exist
        pass

def updateAerealSpeed(icao, speed):
    pass

def updateGndPos(icao, lat, lng):
    pass

def updateGndSpeed(icao, lat, lng):
    pass

def deleteByIcao(icao):
    pass

def handleID(msg):
    msg_icao = pms.adsb.icao(msg)
    srch_res = adsb_collection.find_one({"icao":msg_icao})
    if srch_res == None:
        createEntry(msg)
    else:
        updateTimeStamp(msg_icao)

def updateTimeStamp(icao):
    '''
        just updates the TimeStamp of the icao's data received
    '''
    # plane = adsb_collection.find_one({{"icao":icao}})

    pass


def angleFromCoordinate(lat1,lon1,lat2,lon2) :
    '''
        returns angles in degress between to (lat,long) coordinates
        /n (old_lat, old_lon, new_lat, new_lon)
    '''
    # angle in degrees
    angleDeg = Math.atan2(lon2 - lon1, lat2 - lat1) * 180 / Math.pi
    return angleDeg

def handle_ArealVelocity(msg):
    '''
    Four different subtypes are defined in bits 6-8 of ME field. 
    With subtypes 1 and 2, ground speeds of aircraft are reported. 
    With subtypes 3 and 4, aircraft true airspeed or indicated 
    airspeed are included. Reporting of airspeed in ADS-B only 
    occurs when aircraft position can not be determined based on 
    the GNSS system.
    '''

def handle_data(msg):
    msgTC = pms.adsb.typecode(msg)
    if msgTC in range(9,19) or msgTC in range(20,23): #checking if TC == local aereal position
        print('not updataing yet...')
        updateAerealPos(msg)
    elif msgTC in  range(1,5): #identity typecode
        handleID(msg)
    elif msgTC in range(5,9): #ground position

        # print('ground position')
        print(' ')
    elif msgTC == 19: #airborne velocity
        # print('airborne velocity')
        print(' ')