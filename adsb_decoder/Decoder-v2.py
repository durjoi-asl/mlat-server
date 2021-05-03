import pyModeS as pms
from abc import ABC, abstractmethod, abstractstaticmethod, ABCMeta

class MsgHandler:
    
    def getTC(self):
        pass

    def setTC(self):
        pass

    def loadAction(self):
        pass
    
    @abstractmethod
    def doAction(self):
        pass

class PlaneInfo(metaclass=ABCMeta): #class PlaneInfo(ABC):

    db_Handler = "I handle mongoDB stuff"

    @abstractmethod
    def checkType(self, msg):
        pass
    
    @abstractmethod
    def decodeData(self, msg):
        pass

    def callme(self):
        print("hehe, you called me")

    

    @abstractmethod
    def databaseHandler(self, data):
        pass


class Idendity(PlaneInfo):
    '''
        This class handles all ADSB-identity messages
    '''

    def __init__(self):
        self.myRange = range(1,5)

    def checkType(self, msg):
        if pms.adsb.typecode(msg) in self.myRange:
            print('yes got Identity msg')
            return True

    def decodeData(self, msg):
        '''
            decoding Identity message
        '''

        msg_icao = pms.adsb.icao(msg)
        
        category = pms.adsb.category(msg)
        callsign = pms.adsb.callsign(msg)

        self.databaseHandler([category,callsign])

    def databaseHandler(self, data):
        pass

class ArealPosition(PlaneInfo):
    '''
        This class handles all ADSB-ArealPosition messages
    '''

    def __init__(self):
        self.myRange = [range(9,19), range(20,23)]

    def checkType(self, msg):
        truth = False
        for rng in self.myRange:
            if pms.adsb.typecode(msg) in rng:
                truth = True
        if truth is True:
            print('yes got Areal Position')
            return True

    def decodeData(self, msg, ref_lat, ref_long):
        '''
            decoding Areal Position message
            \n current_lat, currnet_long
        '''
        
        msg_icao = pms.adsb.icao(msg)
        
        new_lt, new_ln = pms.adsb.airborne_position_with_ref( msg, ref_lat, ref_long)
        print("new AEREAL position is lat: {} ,long: {}".format(new_lt, new_ln))

        self.databaseHandler([new_lt, new_ln])

    def databaseHandler(self, data):
        pass

class GroundPosition(PlaneInfo):
    '''
        This class handles all Ground Position messages
    '''

    def __init__(self):
        self.myRange = range(5,9)

    def checkType(self, msg):
        if pms.adsb.typecode(msg) in self.myRange:
            print('yes got Identity msg')
            return True

    def decodeData(self, msg, ref_lat, ref_long):
        '''
            decoding Ground Position message
        '''
        
        msg_icao = pms.adsb.icao(msg)
        
        new_lt, new_ln = pms.adsb.position_with_ref( msg, ref_lat, ref_long)

        print("new GROUND position is lat: {} ,long: {}".format(new_lt, new_ln))

    def databaseHandler(self, data):
        pass



class AirborneVelocity(PlaneInfo):
    '''
        This class handles all Airborne Velocity messages
    '''

    def __init__(self):
        self.myRange = [19]

    def checkType(self, msg):
        if pms.adsb.typecode(msg) in self.myRange:
            print('yes got Identity msg')
            return True

    def decodeData(self, msg, ref_lat, ref_long):
        '''
            decoding Airborne-Velocity message
        '''
        
        msg_icao = pms.adsb.icao(msg)
        data = pms.adsb.velocity(msg) # this is a list => speed, magHeading, verticalSpeed

        self.databaseHandler(data)

    def databaseHandler(self, data):
        pass

class PlaneInfoFactory:

    @staticmethod
    def getInfoClass(msg):
        try:
            msgTC = pms.adsb.typecode(msg)

            if msgTC in range(9,19) or msgTC in range(20,23): #checking if TC == local aereal position
                print("got aereal position msg")
                return ArealPosition()
            elif msgTC in  range(1,5): #identity typecode
                return Idendity()
            elif msgTC in range(5,9): #ground position
                return GroundPosition()
            elif msgTC == 19: #airborne velocity
                return AirborneVelocity()
            
        except AssertionError as _e:
            print(_e)

if __name__ == "__main__":

    airVeloMsg = "8D800B4499091DAD580449E9B053" #type air velocity
    airVeloMsg2 = "8D8013E29920578F18308777CD48" # type air velocity/
    msg = '8D800D0958C387B4297652590A03'
    Areal_Pos = "8D40621D58C382D690C8AC2863A7"
    
    lat_ref = 52.258
    lon_ref = 3.918

    adsbData = "8D4840D6202CC371C32CE0576098"
    adsbME = "202CC371C32CE0"
    gitData = "A00015B4C4600030AA0000B86DD2"

    PLANE = PlaneInfoFactory.getInfoClass(Areal_Pos)
    PLANE.decodeData(msg,lat_ref, lon_ref)
    PLANE.callme()
    print(PLANE.db_Handler)