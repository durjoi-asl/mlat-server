from enum import unique
from os import name
import bson
from flask import Flask, json, jsonify, Response, request, make_response
from flask_sock import Sock
from flask_sqlalchemy.model import Model
import pymongo
from pymongo.common import SERVER_SELECTION_TIMEOUT
from bson.json_util import dumps

from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
import datetime
from functools import wraps

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.wrappers import response

# from flask_migrate import Migrate
# from flask_script import Manager

app = Flask(__name__)
app.secret_key = "hello"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqllite3"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost/testThings'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
sock = Sock(app) # for socket streaming

sqlDB = SQLAlchemy(app)
admin = Admin(app)

# migrate = Migrate(app, sqlDB)
# manager = Manager(app)

MONGOHOST = "localhost" # address where mongoDB is hosted
MONGOPORT = 27017 # port of mondoDB hosting

# FLASKHOST = "192.168.50.12" # address where flask server is hosted and is running
FLASKHOST = "localhost"
FLASKPORT = 5001 # port of flask hosting
DEBUGTRUTH = True # whether in debug mode or not

# app.secret_key = "amar secret" # NOT FOR PRODUCTION, JUST FOR TESTING
app.config['SECRET_KEY'] = 'amar secret'

users_role = sqlDB.Table('user_role',
            sqlDB.Column('user_id',sqlDB.Integer, sqlDB.ForeignKey('users.id')),
            sqlDB.Column('role_id', sqlDB.Integer, sqlDB.ForeignKey('role.role_id')) )

class Users(sqlDB.Model):
    id = sqlDB.Column( sqlDB.Integer, primary_key=True)
    public_id = sqlDB.Column(sqlDB.String(50), unique=True)
    name = sqlDB.Column(sqlDB.String(100))
    password = sqlDB.Column(sqlDB.String(100))
    admin = sqlDB.Column(sqlDB.Boolean)
    roles = sqlDB.relationship('Role', secondary=users_role, backref=sqlDB.backref('persons', lazy='dynamic'))

    # def __init__(self, name, email) -> None:
    #     self.name = name
    #     self.email = email


role_permission = sqlDB.Table('role_permission',
                sqlDB.Column('role_id', sqlDB.Integer, sqlDB.ForeignKey('role.role_id')),
                sqlDB.Column('permission_id', sqlDB.Integer, sqlDB.ForeignKey('permission.permission_id')) )


class Role(sqlDB.Model):
    role_id = sqlDB.Column( sqlDB.Integer, primary_key=True, unique=True)
    role = sqlDB.Column( sqlDB.String(100) )
    permissions = sqlDB.relationship('Permission', secondary=role_permission, backref=sqlDB.backref('roles', lazy='dynamic'))

    @classmethod
    def create(cls, **kw):
        print('create Role')
        # obj = cls(**kw)
        # sqlDB.session.add(obj)
        # sqlDB.session.commit()
    # tag = sqlDB.Column( sqlDB.String(50) )

    # @classmethod
    # def printRoles(cls, **kw):
    #     as = cls.query.all()
    #     print(as)
    #     # obj = cls(**kw)
    #     # sqlDB.session.add(obj)
    #     # sqlDB.session.commit()

        
    # tag = sqlDB.Column( sqlDB.String(50) )


class Permission(sqlDB.Model):
    permission_id = sqlDB.Column( sqlDB.Integer, primary_key=True, unique=True )
    permission  = sqlDB.Column( sqlDB.String(100))
    # tag =  sqlDB.Column( sqlDB.String(50))

admin.add_view(ModelView(Users, sqlDB.session))
admin.add_view(ModelView(Role, sqlDB.session))
admin.add_view(ModelView(Permission, sqlDB.session))
 

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
        user_data['roles'] = user.roles

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

@app.route('/addRolesToUser/<user_id>', methods=['POST'])
def addRolesToUser(user_id):
    data = request.get_json()
    role = data['roles']
    # add role to user_id
    
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
def getRoles(role_id):
    
    role = Role.query.filter_by(role_id = role_id).first()
    if not role:
        return jsonify({"message": "no user found"})
    
    role_data = {}
    role_data['role_id'] = role.role_id
    role_data['role'] = role.role

    return jsonify({"user": role_data})


    

@app.route('/createRole/', methods=["POST"])
def createRole():
    data = request.get_json()
    
    new_role = Role(role=data['role'])
    sqlDB.session.add(new_role)
    sqlDB.session.commit()

    return jsonify({'new_role_created': data['role'], 'role_id': new_role.role_id})

@app.route('/updateRole/<role_id>', methods=['PUT'])
def updateRole(role_id):

    role2update = Role.query.filter_by(role_id = role_id).first()
    if not role2update:
        return jsonify({"message":"no role found"})
    
    data = request.get_json()
    role2update.role = data['role']
    sqlDB.session.commit()

    return jsonify({"message": "the role has been edited"})

@app.route('/deleteRole/<role_id>', methods=["DELETE"])
def deleteRole(role_id):

    role = Role.query.filter_by(role_id=role_id)
    if not role:
        return jsonify({"message":"no role found"})

    sqlDB.session.delete(role)
    sqlDB.session.commit()

    return jsonify({"message": "the role has been deleted"})
    

@app.route('/addPermissionsToRole/<roleId>')
def addPermissionsToRole():
    return 'addPermissionsToRole'

@app.route('/permissions/')
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
def getPermission(permission_id):
    permission = Permission.query.filter_by(permission_id=permission_id).first()

    if not permission:
        return jsonify({"message": "no permission found"})
    
    permission_data = {}
    permission_data['permission_id'] =  permission.permission_id
    permission_data['permission'] =  permission.permission

    return jsonify(permission_data)

@app.route('/permission/create/', methods=["POST"])
def createPermission():
    data = request.get_json()
    new_permission = Permission(permission=data['permission'])
    sqlDB.session.add(new_permission)
    sqlDB.session.commit()
    return jsonify({'message':'new permission created', 'permission': data['permission']})

@app.route('/updatePermission/<permission_id>', methods=["PUT"])
def updatePermission(permission_id):
    data = request.get_json()
   
    find_perm = Permission.query.filter_by(permission_id=permission_id).first()
    if not find_perm:
        return jsonify({'message':'no permission found'})
    
    find_perm.permission = data['permission']
    sqlDB.session.commit()
    
    return jsonify({'message':'permission updated', 'new permission':find_perm})

@app.route('/deletePermission')
def deletePermission():
    return 'deleteRole'

#######################

if __name__ == "__main__":
    sqlDB.create_all()
    app.run(host=FLASKHOST, port=FLASKPORT, debug=DEBUGTRUTH)
    
    