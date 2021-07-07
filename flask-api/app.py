from enum import unique
from os import name
import bson
from flask import Flask, json, jsonify, Response, request, make_response
from flask_sock import Sock
import pymongo
from pymongo.common import SERVER_SELECTION_TIMEOUT
from bson.json_util import dumps
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqllite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
sock = Sock(app) # for socket streaming

sqlDB = SQLAlchemy(app)

MONGOHOST = "localhost" # address where mongoDB is hosted
MONGOPORT = 27017 # port of mondoDB hosting

# FLASKHOST = "192.168.50.12" # address where flask server is hosted and is running
FLASKHOST = "localhost"
FLASKPORT = 5001 # port of flask hosting
DEBUGTRUTH = True # whether in debug mode or not

# app.secret_key = "amar secret" # NOT FOR PRODUCTION, JUST FOR TESTING
app.config['SECRET_KEY'] = 'amar secret'

class Users(sqlDB.Model):
    id = sqlDB.Column( sqlDB.Integer, primary_key=True)
    public_id = sqlDB.Column(sqlDB.String(50), unique=True)
    name = sqlDB.Column(sqlDB.String(100))
    password = sqlDB.Column(sqlDB.String(100))
    admin = sqlDB.Column(sqlDB.Boolean)
    # role = sqlDB.Column(sqlDB.)

    # def __init__(self, name, email) -> None:
    #     self.name = name
    #     self.email = email


try: # establishing mongoDB connection
    mongo = pymongo.MongoClient(
        host=MONGOHOST, 
        port=MONGOPORT,
        serverSelectionTimeoutMS = 2000
        )
    adsb_collection = mongo["planeInfo"]["ADS-B"]
    mongo.server_info() # triggers exception if DB connection can't be established
except:
    print("[ERROR]: DB connection can not be established!!")


def token_required(f): #decorator for authorization
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers['x-access-token'])
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print('token properly decoded:', data)
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : ' Token is invalid'}), 401
        print('current user: ',current_user)
        print('type :',type(current_user))
        return f(current_user, *args, **kwargs)
    
    return decorated

#######################

@app.route("/", methods=["GET"]) # this endpoint returns all data stored in DB and arranges t
def getAllPlanes(): 
    
    data_all = adsb_collection.aggregate( # AGGRETRATE FUNCTION calls all data avilable in ADSB DB collection, then arranges accordingly
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

    return Response( # returning the json data required
        response=dmps,
        status=200,
        mimetype='application/json'
    )

@app.route('/icao/<msg_icao>/', methods=["GET"]) #specific palenInfo endpoint, parameter msg_icao is the icao
def getIcaoPlane(msg_icao):
    # msg_icao = "70E076"
    print(msg_icao)
    icaoData = adsb_collection.aggregate( # this aggregrate function gets a icao number as parameter and 
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

@app.route('/test/auth')
@token_required
def testAuth(current_user):
    user = {
        "name":current_user.name,
        "admin":current_user.admin,
        "password":current_user.password
    }
    return jsonify({"testAPI":"testing", "authoriaztion":"working properly","user who called this":user})

@app.route("/user/", methods=["GET"]) ## implement authorization and authentication to show all users 
def get_all_users():
    users = Users.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        output.append(user_data)
    return jsonify({'users': output})

@app.route("/user/", methods=["POST"]) ## create new user
def create_user():
    print('in create user')
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    sqlDB.session.add(new_user)
    sqlDB.session.commit()
    return jsonify({'message':'new user created', "name":data['name'] })

@app.route("/user/<public_id>", methods=["GET"])
def get_one_user(public_id):

    user = Users.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "no user found"})
    
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({"user": user_data})

@app.route("/user/<public_id>", methods=["DELETE"])
def delete_user(public_id):

    user = Users.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "no user found"})
    
    sqlDB.session.delete(user)
    sqlDB.session.commit()

    return jsonify({"message": "the user has been deleted"})

@app.route("/login/")
def login():
    auth = request.authorization
    print('auth: ', auth)
    print('req: ', request.authorization)

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {"WWW-Authenticate":'Basic realm="Login required!"'})

    user = Users.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('could not verify', 401, {"WWW-Authenticate":'Basic realm="Login required!"'})
    
    if check_password_hash(user.password, auth.password):
        # using pyJwt
        token = jwt.encode({'public_id': user.public_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        # jwt.en
        # token.d
        
        return jsonify({'token':token}) #token.decode('UTF-8')
    
    return make_response('could not verify', 401, {"WWW-Authenticate":'Basic realm="Login required!"'}) # if given name & pass don't match

#######################

if __name__ == "__main__":
    sqlDB.create_all()
    app.run(host=FLASKHOST, port=FLASKPORT, debug=DEBUGTRUTH)
    
    