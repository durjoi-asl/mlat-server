import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hello'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost/testThings'
        # 'postgresql://durjoi:mlat123@localhost/durjoi' 
        
        # dialect+driver://username:password@host:port/database
        
    
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True