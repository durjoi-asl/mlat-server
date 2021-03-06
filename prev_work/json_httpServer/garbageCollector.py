import json
import time
import datetime
from jsonHandler import jsonHandlerClass

def removeSignalLessPlanes():
    '''
        iterates through date to see the timestamp of when each data was updated,
        if last update time from current time is more than 120s then deletes the data
        for teh current plane
    '''
    jsonHandler = jsonHandlerClass()
    data = jsonHandler.getData()
    temp = []
    if data != None:
        for planeData in data:
            timeStamp = datetime.datetime.strptime(planeData["last_updated"], jsonHandler.TIME_FORMAT)
            time_now = datetime.datetime.now()
            diff = (time_now-timeStamp).total_seconds()
            
            print(diff)
            if diff > 120:
                print("MUST DELETE: ", planeData["icao"])
            else:
                print("upto date: ", planeData['icao'])
                temp.append(planeData)

    jsonHandler.write_json(temp)

def run():
    '''
        calls removeSignalLessPlanes();
        
        while True:

        
        time.sleep(60)
        
        removeSignalLessPlanes()
        
        removeSignalLessPlanes() =>
        iterates through date to see the timestamp of when each data was updated,
        if last update time from current time is more than 120s then deletes the data
        for teh current plane
    '''
    while True:
        removeSignalLessPlanes()
        time.sleep(60)


if __name__ == "__main__":
    while True:
        removeSignalLessPlanes()
        time.sleep(60)