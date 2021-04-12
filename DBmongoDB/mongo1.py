'''
    create operations for basic functions, create new entry(just adds callsign and sth), update 
    entry(one for flightInfo the other for gndInfo), update velocity, 
    delete entry and read entry ie CRUD
'''
from pymongo import MongoClient


cluster = MongoClient() #client = MongoClient('localhost', 27017)
print(cluster)

post1 = {
        "icao": "802C09",
        "identity": {
            "category": 1,
            "callsign": "S3AVA___"
        },
        "inflight": True,
        "inGround": False,
        "flightInfo": {
            "lat": 23.8499,
            "long": 90.39256,
            "speed": None,
            "altitude": None,
            "prevPos": {
                "lat": 23.85001,
                "long": 90.39245
            },
            "angle": 146.88865804146374
        },
        "gndInfo": [
            None,
            None,
            None
        ],
        "last_updated": "04/11/2021, 15:47:34"
    }

db = cluster["planeInfo"]
adsb_collection = db['ADS-B']

# adsb_collection.insert_one(post1)

# find many results where condition meets
results = adsb_collection.find({"icao":"702C09"})
for result in results:
    print(result)


print("results: ",results)
print(adsb_collection)