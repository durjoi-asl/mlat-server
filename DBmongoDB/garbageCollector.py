'''
    deletes data in DB if it has existed for more than a specific 
    amount of time without any updates
'''

import json
import time
import datetime
# from jsonHandler import jsonHandlerClass

from pymongo import MongoClient
from bson.json_util import dumps

# from DB_handler import getAllData

def deleteDircraft(icao):
    pass

def removeSignalLessPlanes():
    '''
        iterates through date to see the timestamp of when each data was updated,
        if last update time from current time is more than 120s then deletes the data
        for teh current plane
    '''

    TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"
    cluster = MongoClient() #client = MongoClient('localhost', 27017) by default
    db = cluster["planeInfo"]
    adsb_collection = db['ADS-B']

    cursor = adsb_collection.find()
    list_cur = list(cursor)
    data = list_cur
    # print("type of list_cus: ", type(list_cur))
    # print(list_cur[0]["icao"])

    for planeData in data:
        print('reading planeData in Data')
        timeStamp = datetime.datetime.strptime(planeData["last_updated"], TIME_FORMAT)
        time_now = datetime.datetime.now()
        diff = (time_now-timeStamp).total_seconds()
        data_icao = planeData['icao']

        print("diff",diff)
        if diff > 120:
            print("MUST DELETE: ", planeData["icao"])
            adsb_collection.find_one_and_delete({"icao":data_icao})
        else:
            print("upto date: ", planeData['icao'])
            

    
    
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
        print("testing deletion")
        removeSignalLessPlanes()
        time.sleep(60)
    # removeSignalLessPlanes()