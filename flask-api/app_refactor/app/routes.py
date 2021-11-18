from app import app

from functools import wraps
from flask import  json, jsonify, Response, request, make_response

import jwt 
from bson.json_util import dumps

from app.models import Users, Permission, Role, sqlDB
from app import adsb_collection, historic_collection
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import uuid

from flask_cors import CORS, cross_origin

# from django.blog.blogapi.posts import permissions
CORS(app)



def token_required(f): #decorator for authorization, login
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            print(request.headers['x-access-token'])
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
    
def authRBAC(roles,levels, permissions):
    '''
        params= ( [roles list], [levels list], [permissions list] )

    '''
    def innerRBAC(f):
        '''
        inner decorator for RBAC, checks for roles and permissions
        '''
        @wraps(f)
        def decorated(*args, **kwargs):
            accessMsg = {'accessableFor':{'roles': roles,'levels':levels ,'permissions': permissions}}
            token = request.args.get('token')

            if not token:
                return jsonify({'error': 'Token is missing', 'accessFor':accessMsg['accessableFor'] }), 403
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
            except:
                return jsonify({'error': 'Token is invalid'}), 403

            return f(*args, **kwargs)       
        return decorated  
    return innerRBAC

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
@cross_origin(supports_credentials=True)
def getAllPlanes(): 
    
    data_all = adsb_collection.aggregate( # AGGRETRATE FUNCTION calls all data avilable in ADSB DB collection, then arranges accordingly
        [{
            "$project":{
                "_id": "$icao",
                "cat": "$identity.category",
                "clSgn": "$identity.callsign",
                "typecode":"$identity.typecode",
                "aircraftTypeId":"$identity.aircraftTypeId",
                "aircraftType":"$identity.aircraftType",
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

@app.route("/polyLine/<msg_icao>/", methods=["GET"])
def getPolyLine(msg_icao):
    polyLine = historic_collection.aggregate(
        [
            {"$match":{"icao":msg_icao}},
            {
                "$project":{
                "_id": "$icao",
                "polyLine": "$polyLines",
                "altitude": "$alt"    
                }
            }
        ]
    )

    return  Response(
        response=dumps(polyLine), 
        status=200,
        mimetype='application/json'
    )

@app.route('/icao/<msg_icao>/', methods=["GET"]) #specific palenInfo endpoint, parameter msg_icao is the icao
@cross_origin(supports_credentials=True)
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
                "typecode":"$identity.typecode",
                "aircraftType":"$identity.aircraftType",
                "aircraftTypeId":"$identity.aircraftTypeId",
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
@cross_origin(supports_credentials=True)
@token_required
def testAuth(current_user):
    user = {
        "name":current_user.name,
        "admin":current_user.roles[0],
        "password":"woops you didn't think you'll be able to see this did you? :p"
    }
    return jsonify({"testAPI":"testing", "authoriaztion":"working properly","user who called this":user})

@app.route('/test/auth_role') #finish this
@cross_origin(supports_credentials=True)
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

@app.route('/test/rbac') #finish this
@cross_origin(supports_credentials=True)
@authRBAC(roles=["cook", "baburchi"],levels=[0], permissions=["all", "restricted", "wow"])
def testAuthRbac(current_user):
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
@cross_origin(supports_credentials=True)
def get_all_users():
    users = Users.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        user_data['roles'] = user.roles

        output.append(user_data)
    return jsonify({'users': output})

@app.route("/user/", methods=["POST"]) ## create new user
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
def delete_user(public_id):

    user = Users.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "no user found"})
    
    sqlDB.session.delete(user)
    sqlDB.session.commit()

    return jsonify({"message": "the user has been deleted"})

@app.route("/user/<public_id>", methods=["PUT"])
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
def sign_up():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False, role=0)
    sqlDB.session.add(new_user)
    sqlDB.session.commit()
    return jsonify({'message':'new user created', "name":data['name'] })
    
@app.route("/login/", methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    print('post login')
    data = request.get_json()
    # print("data: ", data)
    # print("username: ",data["username"])
    # print("password: ",data["password"])
    if data == None:
        return make_response('could not verify', 401, {"WWW-Authenticate":'Basic realm="Login required!"'})
    else:
        user = Users.query.filter_by(name=data["username"]).first()
        if user == None:
            return make_response('could not verify', 401, {"WWW-Authenticate":'Basic realm="Login required!"'})
        else:
            
            if check_password_hash(user.password, data['password']):
                token = jwt.encode({'public_id': user.public_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                return jsonify({'token':token}) #token.decode('UTF-8')
            else:
                return make_response('could not verify', 401, {"WWW-Authenticate":'Basic realm="Login required!"'}) # if given name & pass don't match

@app.route("/loginBacicAuth/")
@cross_origin(supports_credentials=True)
def loginBacicAuth():
    print('basic auth login')
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

@app.route('/addRolesToUser/', methods=['POST'])
@cross_origin(supports_credentials=True)
def addRolesToUser():
    return 'addRoles'

@app.route('/roles/')
def getAllRoles():
    
    roles = Role.query.all()
    output = []
    
    for role in roles:
        role_data = {}
        role_data['role_id'] = role.role_id
        role_data['role'] = role.role
        # if role.permission:
        # role_data['permission'] = role.permission
        output.append(role_data)

    return jsonify({"roles": output})

@app.route('/role/<role_id>')
@cross_origin(supports_credentials=True)
def getRoles(role_id):
    
    role = Role.query.filter_by(role_id = role_id).first()
    if not role:
        return jsonify({"message": "no user found"})
    
    role_data = {}
    role_data['role_id'] = role.role_id
    role_data['role'] = role.role

    return jsonify({"user": role_data})


    

@app.route('/role/create/', methods=["POST"])
@cross_origin(supports_credentials=True)
def createRole():
    data = request.get_json()
    
    new_role = Role(role=data['role'])
    sqlDB.session.add(new_role)
    sqlDB.session.commit()

    return jsonify({'new_role_created': data['role'], 'role_id': new_role.role_id})

@app.route('/role/update/<role_id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def updateRole(role_id):

    role2update = Role.query.filter_by(role_id = role_id).first()
    if not role2update:
        return jsonify({"message":"no role found"})
    
    data = request.get_json()
    role2update.role = data['role']
    sqlDB.session.commit()

    return jsonify({"message": "the role has been edited"})

@app.route('/role/delete/<role_id>', methods=["DELETE"])
@cross_origin(supports_credentials=True)
def deleteRole(role_id):

    role = Role.query.filter_by(role_id=role_id)
    if not role:
        return jsonify({"message":"no role found"})

    sqlDB.session.delete(role)
    sqlDB.session.commit()

    return jsonify({"message": "the role has been deleted"})
    

@app.route('/addPermissionsToRole/<roleId>', methods=["POST"])
@cross_origin(supports_credentials=True)
def addPermissionsToRole():
    return 'addPermissionsToRole'

@app.route('/permissions/')
@cross_origin(supports_credentials=True)
def getPermissions():
    permissions = Permission.query.all()
    output = []

    for perm in permissions:
        perm_data = {}
        perm_data['permission_id'] = perm.permission_id
        perm_data['permission'] = perm.permission
        output.append(perm_data)

    return jsonify(output)

@app.route('/permission/<permission_id>')
@cross_origin(supports_credentials=True)
def getPermission(permission_id):
    permission = Permission.query.filter_by(permission_id=permission_id).first()

    if not permission:
        return jsonify({"message": "no permission found"})
    
    permission_data = {}
    permission_data['permission_id'] =  permission.permission_id
    permission_data['permission'] =  permission.permission

    return jsonify(permission_data)

@app.route('/permission/create/', methods=["POST"])
@cross_origin(supports_credentials=True)
def createPermission():
    data = request.get_json()
    new_permission = Permission(permission=data['permission'])
    sqlDB.session.add(new_permission)
    sqlDB.session.commit()
    return jsonify({'message':'new permission created', 'permission': data['permission']})

@app.route('/permission/update/<permission_id>', methods=["PUT"])
@cross_origin(supports_credentials=True)
def updatePermission(permission_id):
    data = request.get_json()
   
    find_perm = Permission.query.filter_by(permission_id=permission_id).first()
    if not find_perm:
        return jsonify({'message':'no permission found'})
    
    find_perm.permission = data['permission']
    sqlDB.session.commit()
    
    return jsonify({'message':'permission updated', 'new permission':find_perm})

@app.route('/permission/delete/<permission_id>')
@cross_origin(supports_credentials=True)
def deletePermission():
    return 'deleteRole'