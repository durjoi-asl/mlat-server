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

import datetime


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from model import  sqlDB

# from flask_migrate import Migrate
# from flask_script import Manager

app = Flask(__name__)
app.secret_key = "hello"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqllite3"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost/testThings'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
sock = Sock(app) # for socket streaming




# migrate = Migrate(app, sqlDB)
# manager = Manager(app)

MONGOHOST = "localhost" # address where mongoDB is hosted
MONGOPORT = 27017 # port of mondoDB hosting

# FLASKHOST = "192.168.50.12" # address where flask server is hosted and is running
FLASKHOST = "localhost"
FLASKPORT = 9001 # port of flask hosting
DEBUGTRUTH = True # whether in debug mode or not

# app.secret_key = "amar secret" # NOT FOR PRODUCTION, JUST FOR TESTING
app.config['SECRET_KEY'] = 'amar secret'


from routes import *


#######################

if __name__ == "__main__":
    sqlDB.create_all()
    app.run(host=FLASKHOST, port=FLASKPORT, debug=DEBUGTRUTH)
    
    