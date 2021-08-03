from app import app 

from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
import datetime

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app import sqlDB 
# from app import adsb_collection
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
    # tag = sqlDB.Column( sqlDB.String(50) )


class Permission(sqlDB.Model):
    permission_id = sqlDB.Column( sqlDB.Integer, primary_key=True, unique=True )
    permission  = sqlDB.Column( sqlDB.String(100))
    # tag =  sqlDB.Column( sqlDB.String(50))

admin.add_view(ModelView(Users, sqlDB.session))
admin.add_view(ModelView(Role, sqlDB.session))
admin.add_view(ModelView(Permission, sqlDB.session))
 