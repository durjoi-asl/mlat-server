import pyModeS as pms

class adsb_decoder:
    '''
        ADSB decoding wrapper
    '''


    def __init__(self, lat_ref, long_ref):
        self.lat_ref = lat_ref
        self.lon_ref = lon_ref

    def identify(self, msg):
        '''
        gets identity of adsb data, only done when typeCode(TC) == 1 to 4 
        \n returns (category, callsign)
        '''
        category = pms.adsb.category(msg)
        callsign = pms.adsb.callsign(msg)
        # idcode = pms.idcode(msg)
        print('category: ', category)
        print('callsign: ', callsign) 

        return (category, callsign)

    def getGlobalAirPos(self):
        '''
               # a pair of odd and even messages required to calculate the position
               \n # not sure how to implement this so have not implemented this, DO NOT USE THIS
        '''
        
        print("--------- Global air position ---------")
        msg0 = "8D40621D58C382D690C8AC2863A7"
        msg1 = "8D40621D58C386435CC412692AD6"
        t0 = 1457996402
        t1 = 1457996400
        position = pms.adsb.position(msg0, msg1, t0, t1)
        print('position: ', position)

        msg = "8D40621D58C382D690C8AC2863A7"
        lat_ref = 52.258
        lon_ref = 3.918
        position2 = pms.adsb.position_with_ref(msg, lat_ref, lon_ref)
        print('position2: ', position2)
        print("--------- end air position ---------")

    def getLocalAirPos(self, msg):
        '''
        returns lat long, just provide the mode-s long data
        \n point of reference is the lat,lon of the antaena that receives the singal
        '''

        # position = pms.adsb.position_with_ref(msg, lat_ref, lon_ref)
        position = pms.adsb.position_with_ref(msg, self.lat_ref, self.lon_ref)
        
        return position

    def getGNSSheight(self, msg):
        '''
        if TC == 20-22 then only GNSS height possible
        \n returns ground pos, params = point of reference ie the lat,lon of the antaena that receives the singal
        '''

        altitude = pms.adsb.altitude(msg)
        print('GNSS altitute: ', altitude)

        return altitude

    def getDF(self, buff):
        '''
        receives hex-msg string and returns the DF-code (Downlink Format)
        '''

        binNum = bin(int(buff[0:2],16))
        print(binNum)
        DFcode = int(binNum[0:7],2)
        print("DFcode: ", DFcode)

        return DFcode

    def getTC(self, buff):
        '''
        \n gets hex-msg string as param and returns the type-code; 
        \n tc == 1-4  => aiircraft idendity; 
        \n tc == 5-8  => sufrace position; 
        \n tc == 9-18, 20-22  => airborne position; 
        \n tc == 19  => airborne velocity
        '''

        tc = pms.adsb.typecode(buff)
        print("Type Code: ",tc)

        return tc

    def getGndPosition(self, msg):
        '''
        takes adsb hex-code and returns local surface location
        '''

        # position = pms.adsb.position_with_ref(msg, lat_ref, lon_ref)
        position = pms.adsb.position_with_ref(msg, self.lat_ref, self.lat_ref)

        return position

    def runTest(self, adsbData):
        pms.tell(adsbData)
        
        # print(pms.hex2bin(adsbME))
        self.getGlobalAirPos()
        # print(pms.hex2bin(adsbME))
        # getLocalAirPos(msg0)

        self.getGNSSheight(adsbData)

        # print(pms.hex2bin(adsbME))
        self.identify(adsbData)

        print('flag: ', pms.adsb.oe_flag(adsbData)) # to get flag(+ve OR -ve)

        print('category: ', pms.adsb.category(adsbData))



    def getAirbornePos(self, msg):
        '''
            local airborne position
        '''

        # pos = pms.adsb.position_with_ref(msg, self.lat_ref, self.lon_ref)
        pos = pms.adsb.airborne_position_with_ref(msg, self.lat_ref, self.lon_ref)

        return pos

    def getAirVelocity(self, msg):
        '''
            Four different subtypes are defined in bits 6-8 of ME field. 
            With subtypes 1 and 2, ground speeds of aircraft are reported. 
            With subtypes 3 and 4, aircraft true airspeed or indicated 
            airspeed are included. Reporting of airspeed in ADS-B only 
            occurs when aircraft position can not be determined based on 
            the GNSS system.
            type:1,2 = Gnd Speed
            type:3,4 = True airspeed/indicated airspeed
            tupe:2,4 for supersonic aircraft, but they don't exist now, similat format to type 1,3
            
            \n returns a list
            \n list[0]=speed, list[1]=magHeading, list[2]=verticalSpeed
        '''

        vel = pms.adsb.velocity(msg)
        # print('air velocity: ', vel)

        return vel



    def decodeAdsbData(self, buff):
        '''
        receives adsb code as buff in params and its type code as msgTC, then decrypts the adsb data
        '''

        msgTC = pms.adsb.typecode(buff)
        print('icao: ', pms.adsb.icao(buff))
        if 1 <= msgTC <= 4:
            # aircraft identity
            planeId = self.identify(buff)
            print('air craft ID: ', planeId)
        elif 5 <= msgTC <= 8:
            # ground position
            pos = self.getGndPosition(buff)
            print('ground position: ', pos)
        elif 9 <= msgTC <= 18 or 20 <= msgTC <= 22:
            # airborne position
            pos = self.getAirbornePos(buff)
            print('airborne position: ', pos)
        elif msgTC == 19:
            # airborne velocity
            airVel = self.getAirVelocity(buff)
            print('air velocity: ', airVel)
            

# decodeAdsbData(adsbData)





if __name__ == "__main__":

    print('testing test data')

    # msg = "8D40621D58C382D690C8AC2863A7"
    airVeloMsg = "8D800B4499091DAD580449E9B053" #type air velocity
    airVeloMsg2 = "8D8013E29920578F18308777CD48" # type air velocity/
    msg = '8D800D0958C387B4297652590A03'
    
    lat_ref = 52.258
    lon_ref = 3.918

    localAdsbDecoder = adsb_decoder(lat_ref, lon_ref)
    


    msg1, msg2 = ',','12'

    adsbData = "8D4840D6202CC371C32CE0576098"
    adsbME = "202CC371C32CE0"

    gitData = "A00015B4C4600030AA0000B86DD2"

    # position = pms.adsb.position_with_ref(msg, lat_ref, lon_ref)
    # print(position)

    localAdsbDecoder.decodeAdsbData(msg)
    # pms.tell(msg)
    tc = localAdsbDecoder.getTC(msg)
    # print(type(tc))
    print("type code: ", tc )

    category = pms.adsb.category("8D4840D6202CC371C32CE0576098")
    print('cat: ',category)

    # callsign = pms.adsb.callsign(msg)
    # print('call: ',callsign)

    localAdsbDecoder.decodeAdsbData(msg)