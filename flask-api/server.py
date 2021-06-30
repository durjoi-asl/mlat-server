import bson
from flask import Flask, jsonify, Response
from flask_sock import Sock
import pymongo
from pymongo.common import SERVER_SELECTION_TIMEOUT
from bson.json_util import dumps

app = Flask(__name__)
sock = Sock(app)

MONGOHOST = "localhost"
MONGOPORT = 27017

try:
    mongo = pymongo.MongoClient(
        host=MONGOHOST, 
        port=MONGOPORT,
        serverSelectionTimeoutMS = 2000
        )
    adsb_collection = mongo["planeInfo"]["ADS-B"]
    mongo.server_info() # triggers exception if DB connection can't be established
except:
    print("[ERROR]: DB connection can not be established!!")

#######################

@app.route("/", methods=["GET"])
def getAllPlanes():
    data_all = adsb_collection.aggregate(
        [{
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
                    "$cond":{ "if": { "$eq": ["$inflight", True] }, "then": "$flightInfo.altitude", "else": "$gndInfo.angle" }
                    },
                "angle": "$flightInfo.angle"
            }
        }]
        )

    
    # dmps = dumps(adsb_collection.find())
    dmps = dumps(data_all)
    
    # cursor = adsb_collection.find()
    # list_cur = list(cursor)
    # json_str = dumps(list_cur)

    return Response(
        response=dmps,
        status=200,
        mimetype='application/json'
    )

@app.route('/icao/<msg_icao>', methods=["GET"]) #specific palenInfo
def getIcaoPlane(msg_icao):
    # msg_icao = "70E076"
    print(msg_icao)
    icaoData = adsb_collection.aggregate(
        [
            {"$match":{"icao":msg_icao}},
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
                "speed": {
                    "$cond":{ "if": { "$eq": ["$inflight", True] }, "then": "$flightInfo.velocity.speed", "else": "$gndInfo.speed" }
                    },
                
                "mag": {
                        "$cond":[  { "$eq": ["$inflight", True]}, "$flightInfo.velocity.magHeading", "$$REMOVE"  ]
                        },
                # "mag00": "$flightInfo.velocity.magHeading",
                "vSpeed": "$flightInfo.velocity.verticalSpeed",
                "alt": {
                    "$cond":{ "if": { "$eq": ["$inflight", True] }, "then": "$flightInfo.altitude", "else": "$gndInfo.angle" }
                    },
                "angle": "$flightInfo.angle",
            }
        }]
        )
    return  Response(
        response=dumps(icaoData),
        status=200,
        mimetype='application/json'
    )

#######################

if __name__ == "__main__":
    app.run(host="192.168.50.12",port=5001, debug=True)
    # app.run