# ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__',
#  '__path__', '__spec__', 'adsb', 'aero', 'allcall', 'allzeros', 'altcode', 'altitude', 'bds', 
#  'bin2hex', 'bin2int', 'c_common', 'commb', 'common', 'cprNL', 'crc', 'data', 'decoder', 'df', 'dirpath', 
#  'extra', 'floor', 'gray2alt', 'hex2bin', 'hex2int', 'icao', 'idcode', 'is_icao_assigned', 'os', 'squawk',
#   'surv', 'tcpclient', 'tell', 'typecode', 'warnings', 'wrongstatus']
'''
    practicing decoding mlat messages
    not using this anywhere, it's like a wrapper for pyModeS
'''
import pyModeS as pms
import jsonHandler
msg1, msg2 = ',','12'
adsbData = "8D4840D6202CC371C32CE0576098"
adsbME = "202CC371C32CE0"

gitData = "A00015B4C4600030AA0000B86DD2"

lat_ref = 52.258
lon_ref = 3.918

def identify(msg):
    '''
    gets identity of adsb data, only done when typeCode(TC)==1-4 
    \n returns (category, callsign)
    '''
    category = pms.adsb.category(msg)
    callsign = pms.adsb.callsign(msg)
    # ican = pms.adsb.icao(msg)
    # typecode = pms.typecode(msg)
    # idcode = pms.idcode(msg)
    print('category: ', category)
    print('callsign: ', callsign) #
    # print('ican: ', ican) #
    # print('typecode: ', typecode) #
    return (category, callsign)

def getGlobalAirPos():
    # a pair of odd and even messages required to calculate the position
    print("--------- air position ---------")
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

def getLocalAirPos(msg):
    '''
    returns lat long, just provide the mode-s long data
    \n point of reference is the lat,lon of the antaena that receives the singal
    '''
    position = pms.adsb.position_with_ref(msg, lat_ref, lon_ref)
    return position

def getGNSSheight():
    '''
    if TC == 20-22 then only GNSS height possible
    \n returns ground pos, params = point of reference ie the lat,lon of the antaena that receives the singal
    '''
    
    msg = "8D40621D58C382D690C8AC2863A7"
    altitude = pms.adsb.altitude(msg)
    print('GNSS altitute: ', altitude)

def getDF(buff):
    '''
    receives hex-msg string and returns the DF-code (Downlink Format)
    '''
    binNum = bin(int(buff[0:2],16))
    print(binNum)
    DFcode = int(binNum[0:7],2)
    print("DFcode: ", DFcode)
    return DFcode

def getTC(buff):
    '''
    gets hex-msg string as param and returns the type-code; 
    \n tc == 1-4  => aiircraft idendity; 
    \n tc == 5-8  => sufrace position; 
    \n tc == 9-18, 20-22  => airborne position; 
    \n tc == 19  => airborne velocity
    '''
    tc = pms.adsb.typecode(buff)
    print(tc)
    return tc

def getGndPosition(msg):
    '''
    takes adsb hex-code and returns local surface location
    '''
    position = pms.adsb.position_with_ref(msg, lat_ref, lon_ref)
    return position

def runTest():
    pms.tell(adsbData)

    # print(pms.hex2bin(adsbME))
    getGlobalAirPos()
    # print(pms.hex2bin(adsbME))
    # getLocalAirPos(msg0)
    getGNSSheight()
    # print(pms.hex2bin(adsbME))
    identify(adsbData)

    print('flag: ', pms.adsb.oe_flag(adsbData)) # to get flag(+ve OR -ve)

    print('category: ', pms.adsb.category(adsbData))

# runTest()
# getDF(adsbData)




### to get flag(+ve OR -ve)  ===> pms.adsb.oe_flag(adsbData)

bs_lat = 23.83588
bs_long = 90.41611

def getAirbornePos(msg):
    pos = pms.adsb.position_with_ref(msg, bs_lat, bs_long)
    return pos


def decryptAdsbData(buff):
    '''
    receives adsb code as buff in params and its type code as tcCode, then decrypts the adsb data
    '''
    # pos = pms.adsb.position_with_ref(buff, bs_lat, bs_long)
    # print('position: ', pos)

    # if getDF(buff) == 17:
    ## so the message type we get is ADSB
    tcCode = pms.adsb.typecode(buff)
    print('icao: ', pms.adsb.icao(buff))
    if 1 <= tcCode <= 4:
        # aircraft identity
        planeId = identify(msg)
        print('air craft ID: ', planeId)
    elif 5 <= tcCode <= 8:
        # surface position
        pos = getGndPosition(buff)
        print('ground position: ', pos)
    elif 9 <= tcCode <= 18 or 20 <= tcCode <= 22:
        # airborne position
        pos = getAirbornePos(buff)
        print('airborne position: ', pos)
    elif tcCode == 19:
        # airborne velocity
        pass

# decryptAdsbData(adsbData)


# msg = "8D40621D58C382D690C8AC2863A7"
# msg = "8D800B4499091DAD580449E9B053" #type air velocity
# msg = "8D8013E29920578F18308777CD48" # type air velocity/
msg = '8D800D0958C387B4297652590A03'


if __name__ == "__main__":
    print('yoyo ')
    # position = pms.adsb.position_with_ref(msg, lat_ref, lon_ref)
    # print(position)

    decryptAdsbData(msg)
    # pms.tell(msg)
    tc = getTC(msg)
    # print(type(tc))
    # print("type code: ", tc )

    category = pms.adsb.category("8D4840D6202CC371C32CE0576098")
    callsign = pms.adsb.callsign(msg)
    print('cat: ',category)
    print('call: ',callsign)

    identify(msg)