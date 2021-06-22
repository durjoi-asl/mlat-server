from pymongo import MongoClient
import pyModeS as pms
import datetime
import math as Math
from bson.json_util import dumps

from pymongo import MongoClient

cluster_instance = MongoClient()["planeInfo"]["ADS-B"] #client = MongoClient('localhost', 27017)

cursor = cluster_instance.aggregate(
    [
        {"$match":{"icao":"4B846D"}},
        {
        "$project":{
            "_id": "$icao",
            "cat": "$identity.category",
            "clSgn": "$identity.callsign",
            "fly": "$inflight",
            "lat": {
                "$cond":{ "if": { "$eq": ["$inflight", True] }, "then": "$flightInfo.lat", "else": "$gndInfo.lat" }
                },
            "lon": {
                "$cond":{ "if": { "$eq": ["$inflight", True] }, "then": "$flightInfo.long", "else": "$gndInfo.long" }
                },
            # get speed if aircraft is in flight
            "speed": {
                "$cond":{ "if": { "$eq": ["$inflight", True] }, "then": "$flightInfo.velocity.speed", "else": "$gndInfo.speed" }
                },
            
            "mag": {
                    "$cond":[  { "$eq": ["$inflight", True]}, "$flightInfo.velocity.magHeading", "$$REMOVE"  ]
                    },
            "mag00": "$flightInfo.velocity.magHeading",
            "vSpeed": "$flightInfo.velocity.verticalSpeed",
            "alt": {
                "$cond":{ "if": { "$eq": ["$inflight", True] }, "then": "$flightInfo.angle", "else": "$gndInfo.angle" }
                },
            "angle": "$flightInfo.angle",
        }
    }]
    )

# cursor = cluster_instance.find(
#      {"icao":"8013DE"},{"_id":0, "host":1}
# )
# ,{"host":1, "icao":1}
print("cursor")
print(cursor)
list_cur = list(cursor)
data = dumps(list_cur)

print(data)
# print(data[0]["icao"])
print(list_cur)
# print(list_cur[0]["host"]=='192.168.101.3')
# print(list_cur[0]["host"])

