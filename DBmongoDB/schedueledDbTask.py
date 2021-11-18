'''
    this runs the grabageCollector and interpolation scripts
    interpolate aircraft line for 5 minutes if no signal received, then after that hand it over to garbage collector
    Time diff <= 5mins and >30seconds : Interpolate
    Time diff > 5mins : GarbageCollector
    handles airborne aircrafts
'''

import time
import datetime
from DB_Connection import getADSBcollection
from interpolate import interpolate

TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"
adsbCollection = getADSBcollection()

def startScheduledTask():
    
    while True:
        cursor = adsbCollection.find()
        list_cur = list(cursor)
        data = list_cur
        
        for planeData in data:
            
            timeStamp = datetime.datetime.strptime(planeData["last_updated"], TIME_FORMAT)
            time_now = datetime.datetime.now()
            diff = (time_now-timeStamp).total_seconds()
            data_icao = planeData['icao']

            lat = planeData["flightInfo"]["lat"]
            long = planeData["flightInfo"]["long"]
            angle = planeData["flightInfo"]["angle"]
            print('difference in time for : ', diff)
            
            if diff > 300:
                print("DELETING: " + planeData['icao'] + " ,signal not received for greater than 5 mins")
                adsbCollection.find_one_and_delete({"icao":data_icao})
            elif diff > 30 and diff <= 300  and lat != None and long != None:
                print("INTERPOLATING: ", planeData["icao"])
                
                newLat, newLong = interpolate(lat, long, angle)
                adsbCollection.find_one_and_update({"icao":data_icao},{'$set':{"flightInfo.lat":newLat, "flightInfo.long":newLong}})
            else:
                print('Do Nothing for: {}'.format(data_icao))
        
        time.sleep(5)

if __name__ == "__main__":
    startScheduledTask()