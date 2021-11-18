from pymongo import MongoClient

import time

cluster = MongoClient() #client = MongoClient('localhost', 27017) by default
adsbDb = cluster["planeInfo"]
adsb_collection = adsbDb['ADS-B']

historyDb = cluster["planeInfo"]
flightHistory_collection = historyDb['flightHistory']


def getAdsbData():
    cursor = adsb_collection.find()
    listAdsbData = list(cursor)
    
    return listAdsbData

def updateHistory():
    
    adsbData = getAdsbData()

    cursor = flightHistory_collection.find()
    HistoryDataList = list(cursor)

    for aircraft in adsbData:
        icao = aircraft['icao']
        if flightHistory_collection.find_one({"icao":aircraft['icao']}) != None:    
            print('aircraft {icao} exists and updating')
            # if aircraft exists in historical data
            lat = aircraft['flightInfo']['lat']
            long = aircraft['flightInfo']['long']
            alt  = aircraft['flightInfo']['altitude']
            
            histLastPos = flightHistory_collection.find_one({"icao":"800C12"})['polyLines'][-1]
            if lat != None and long != None and alt != None and lat != histLastPos[0] and long != histLastPos[1]:
                # lat, long and alt from DB should not be None 
                # and the last historic position saved should not be equal to the new position fetched from the DB
                flightHistory_collection.update_one({'icao':icao},{"$push":{"polyLines":[lat,long] } } )
                # updates polyLines
                flightHistory_collection.update_one({'icao':icao}, {'$push':{"altitude":alt}})
        else:
            # aircraft doesn't exist in hostorical data

            print('creating new Historic entry for aircraft {icao}')
            
            lat = aircraft['flightInfo']['lat']
            long = aircraft['flightInfo']['long']
            alt = aircraft['flightInfo']['altitude']
            
            newAircraft={
                "icao":icao,
                "polyLines":[[lat,long]],
                "altitude": [alt]
            }
            
            flightHistory_collection.insert_one(newAircraft)

def run():
    while True:
        updateHistory()
        print('halting for 60 secs')
        time.sleep(60)


if __name__ == "__main__":
    run()