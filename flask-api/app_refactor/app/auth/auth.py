from functools import wraps
from flask import  config, json, jsonify, request
import jwt 
from app import Config
print(Config)
# from app.models import Users, Permission, Role, sqlDB

# def token_required(f): #decorator for authorization
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         print(request.headers['x-access-token'])
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']

#         if not token:
#             return jsonify({'message': 'token is missing'}), 401
        
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#             print('token properly decoded:', data)
#             current_user = Users.query.filter_by(public_id=data['public_id']).first()
#         except:
#             return jsonify({'message' : ' Token is invalid'}), 401
#         print('current user: ',current_user)
#         print('type :',type(current_user))
#         return f(current_user, *args, **kwargs)
    
#     return decorated

# def get_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
        
#         if not token:
#             return jsonify({'message': 'token is missing'}), 401

#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#             print('token property decoded: ', data)
#             current_user = Users.query.filter_by(public_id=data['public_id']).first()
#         except:
#             return jsonify({'message': 'Token is invalid'}), 401