from .aircraftType import checkAircraftType
import datetime
from .handler_raw_data import getCA, getDF, getParity, getME
from .structureIdentity import getIdStructureFromHexData

def create_new_aircraft_object(data, host, TIME_FORMAT):
    '''
    creates new aircraft object and returns it
    
    '''
    
    aircraftType = checkAircraftType(data[3], data[1])
    aircraftIdStructure = getIdStructureFromHexData(data[4][0])
    aircraft = {
            "icao": data[0],
            "identity":{
                "category":data[1],
                "callsign":data[2],
                "typecode":data[3],
                "aircraftType": aircraftType[0],
                "aircraftTypeId": aircraftType[1]
                },
            "inflight": False,
            "inGround": False,
            "flightInfo": {
                "odd_frame":None,
                "even_frame":None,
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
            "last_updated": datetime.datetime.now().strftime(TIME_FORMAT),
            "host": host,
            "raw":{
                "signal":{
                    "hexcode":data[4][0],
                    "timestamp":data[4][1]
                },
                "decoded_hex":{
                    "DF":getDF(data[4][0]),
                    "CA":getCA(data[4][0]),
                    "ICAO":data[0],
                    "ME":getME(data[4][0]),
                    "PI":getParity(data[4][0])
                },
                "decoded_msg":{
                    "msg_type":"Aircraft_identification_and_category",
                    "msg":{
                        "TC":aircraftIdStructure[0],
                        "CA":aircraftIdStructure[1],
                        "C1":aircraftIdStructure[2],
                        "C2":aircraftIdStructure[3],
                        "C3":aircraftIdStructure[4],
                        "C4":aircraftIdStructure[5],
                        "C5":aircraftIdStructure[6],
                        "C6":aircraftIdStructure[7],
                        "C7":aircraftIdStructure[8],
                        "C8":aircraftIdStructure[9],
                    }
                }
            }
        }

    return aircraft