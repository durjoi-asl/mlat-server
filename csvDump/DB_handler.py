from pymongo import MongoClient

cluster = MongoClient() #client = MongoClient('localhost', 27017) by default
db = cluster["planeInfo"]
adsb_collection = db['ADS-B']

def findByIcao(icao):
    cursor = adsb_collection.find({"icao":icao})
    list_cur = list(cursor)
    data = list_cur
   
    return [ data[0]["icao"], str(data[0]["identity"]), data[0]["inflight"],data[0]["inGround"], data[0]["flightInfo"]["lat"],  data[0]["flightInfo"]["long"], data[0]["flightInfo"]["velocity"]["speed"], data[0]["flightInfo"]["velocity"]["magHeading"],  data[0]["flightInfo"]["velocity"]["verticalSpeed"],data[0]["flightInfo"]["altitude"],data[0]["flightInfo"]["angle"],  data[0]["gndInfo"]["lat"], data[0]["gndInfo"]["long"], data[0]["gndInfo"]["speed"], data[0]["gndInfo"]["altitude"], data[0]["raw"]["signal"]["hexcode"], data[0]["raw"]["signal"]["timestamp"], str(data[0]["raw"]["decoded_hex"]), str(data[0]["raw"]["decoded_msg"]["msg_type"]), str([data[0]["raw"]["decoded_msg"]["msg"]])  ]
   


if __name__ == "__main__":
    findByIcao("800C09")