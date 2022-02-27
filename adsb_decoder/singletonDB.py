from abc import ABCMeta, abstractstaticmethod 
from pymongo import MongoClient

class IMongoConnection(metaclass=ABCMeta):
    '''
    MongoDB connection interface
    '''

    @abstractstaticmethod
    def get_connection():
        """implement in child class"""


class MongoConnectionSingleton(IMongoConnection):

    __cluster_instance = None

    @staticmethod
    def get_instance():
        if MongoConnectionSingleton.__cluster_instance == None:
            MongoConnectionSingleton('Default Name')
        return MongoConnectionSingleton.__cluster_instance

    def __init__(self, name):
        if MongoConnectionSingleton.__cluster_instance != None:
            raise Exception("singleton cannot be instantiated more than once")
        else:
            #creating client/cluster 
            self.name = name
            MongoConnectionSingleton.__cluster_instance = MongoClient()["planeInfo"]["ADS-B"] #client = MongoClient('localhost', 27017)
            print("mongo created")
    
    @staticmethod
    def get_connection():
        print(f"## Name of DB: {MongoConnectionSingleton.__cluster_instance}")
        # print(f"Name of DB: {self.name}")

if __name__ == "__main__" :
    '''
    not for deployment
    just for testing
    '''
    db = MongoConnectionSingleton('Saadat')
    print(db)
    db.get_connection()

    db2 = MongoConnectionSingleton.get_instance()
    print(db2)

    db3 = MongoConnectionSingleton.get_instance()
    print(db3)