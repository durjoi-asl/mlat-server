from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import pymongo
from pymongo.common import SERVER_SELECTION_TIMEOUT
from bson.json_util import dumps

from app import app
sqlDB = SQLAlchemy(app)
admin = Admin(app)

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
