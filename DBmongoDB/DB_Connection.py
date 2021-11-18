'''
    for connecting to mongoDB and its cluster
'''
from pymongo import MongoClient

def getPlaneInfoDB():
    '''
        connects to mongoDB and returns planeInfo Database
    '''
    client = MongoClient() #client = MongoClient('localhost', 27017) by default
    db = client["planeInfo"]
    return db

def getADSBcollection():
    '''
        returns ADSB collection
    '''
    db = getPlaneInfoDB()
    adsb_collection = db['ADS-B']
    return adsb_collection

def getFlightHistoryCollection():
    db = getPlaneInfoDB()
    flightHistory_collection = db['flightHistory']
    return flightHistory_collection