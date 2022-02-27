import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hello'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://titas:titu12345@localhost/mlat_db'
        # 'postgresql://durjoi:mlat123@localhost/durjoi' 
        
        # dialect+driver://username:password@host:port/database
        
    
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True