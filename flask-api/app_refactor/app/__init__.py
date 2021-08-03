from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

import pymongo
sqlDB = SQLAlchemy(app)
migrate = Migrate(app, sqlDB)

MONGOHOST = "localhost" # address where mongoDB is hosted
MONGOPORT = 27017 # port of mondoDB hosting

try: # establishing mongoDB connection
    mongo = pymongo.MongoClient(
        host=MONGOHOST, 
        port=MONGOPORT,
        serverSelectionTimeoutMS = 2000
        )
    adsb_collection = mongo["planeInfo"]["ADS-B"]
    mongo.server_info() # triggers exception if DB connection can't be established
    print("[SUCCESS]: mongo-DB connection established")
except:
    print("[ERROR]: mongo-DB connection can not be established!!")

from app import routes, models