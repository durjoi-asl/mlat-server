from pymongo import MongoClient
from DB_Connection import getFlightHistoryCollection, getADSBcollection
import time


adsb_collection = getADSBcollection()
flightHistory_collection = getFlightHistoryCollection()


def getAdsbData():
    cursor = adsb_collection.find()
    listAdsbData = list(cursor)
    
    return listAdsbData

def updateHistory():
    
    adsbData = getAdsbData()

    # cursor = flightHistory_collection.find()
    # HistoryDataList = list(cursor)

    for aircraft in adsbData:
        icao = aircraft['icao']
        
        newLat = aircraft['flightInfo']['lat']
        newLong = aircraft['flightInfo']['long']
        newAlt  = aircraft['flightInfo']['altitude']

        if flightHistory_collection.find_one({"icao":icao}) != None:  
            # check if adsb icao data already exists, if exists then push new position
            # if new position is same as last updated position then don't update
            print('aircraft {} exists and updating'.format(icao))
            # if aircraft exists in historical data
            
            histLastPos = flightHistory_collection.find_one({"icao":icao})['polyLines'][-1]
            if newLat != None and newLong != None and newAlt != None and newLat != histLastPos[0] and newLong != histLastPos[1]:
                # lat, long and alt from DB should not be None 
                # and the last historic position saved should not be equal to the new position fetched from the DB

                # update polyLines
                flightHistory_collection.update_one({'icao':icao},{"$push":{"polyLines":[newLat,newLong] } } )
                # updates altitude
                flightHistory_collection.update_one({'icao':icao}, {'$push':{"altitude":newAlt}})
            else:
                pass
        else:
            # aircraft doesn't exist in hostorical data
            # so create new document
            print('creating new Historic entry for aircraft {}'.format(icao))
            
            newAircraft={
                "icao":icao,
                "polyLines":[[newLat,newLong]],
                "altitude": [newAlt]
            }
            
            flightHistory_collection.insert_one(newAircraft)

def run():
    while True:
        updateHistory()
        print('halting for 60 secs')
        time.sleep(2)
        print(time.time)

if __name__ == "__main__":
    run()
    