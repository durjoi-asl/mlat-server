from app import app

from functools import wraps
from flask import  json, jsonify, Response, request, make_response

import jwt 
from bson.json_util import dumps

from model import Users, Permission, Role, adsb_collection, sqlDB
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import uuid

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

def get_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print('token property decoded: ', data)
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
  

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
        "password":"woops you didn't think you'll be able to see this did you? :p"
    }
    return jsonify({"testAPI":"testing", "authoriaztion":"working properly","user who called this":user})

@app.route('/test_auth_role') #finish this
@token_required
def testAuthRole(current_user):
    # print(current_user)
    if current_user.role == 2:
        user = {
            "name":current_user.name,
            "admin":current_user.admin,
            "role" : current_user.role,
            "password":"woops you didn't think you'll be able to see this did you? :p"
        }
    return jsonify({"testAPI":"testing roles", "authoriaztion":"working properly","user who called this":user})



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
        # user_data['role'] = user.role

        output.append(user_data)
    return jsonify({'users': output})

@app.route("/user/", methods=["POST"]) ## create new user
def create_user():
    print('in create user')
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    print('to create, admin level:')
    print(data['admin'])
    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=data['admin'])
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

@app.route("/user/<public_id>", methods=["PUT"])
@token_required
def updateUser(current_user, public_id):
    if current_user.public_id != public_id and  current_user.admin != True:
        print(current_user.admin)
        return jsonify({"message": "you don't have authorization"})
    else:
        user2update = Users.query.filter_by(public_id=public_id).first()
        if not user2update:
            return jsonify({"message":"no user found"})

        data = request.get_json()
        user2update.name = data['name']
        # user2update.password = data['password']
        sqlDB.session.commit()
        return jsonify({"message": "the user has been edited"})



@app.route("/signup/", methods=["POST"]) #normal user role=0, admin=False
def sign_up():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False, role=0)
    sqlDB.session.add(new_user)
    sqlDB.session.commit()
    return jsonify({'message':'new user created', "name":data['name'] })
    

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
