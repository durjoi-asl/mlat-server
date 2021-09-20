'''
    for testing/practicing mode-S long decoding using pyModeS library
'''
import pyModeS as pms
adsbData = "8D4840D6202CC371C32CE0576098"
# data = pms.tell("8D4840D6202CC371C32CE0576098")

def calcLong():
    pass

def calcLat():
    pass

def getGeneralInfo():
    # print(dir(data))
    # print(data)
    # print('type: ',type(data))

    # li = ['02E617B0AE1956', '0F320768D8872B'] # mode-s short
    # li = ['02A18630596A43', '0FE1148D6FEA5F']
    # li = ['5D8013DE781C06', '10869C76C7E422']
    li = ['8D76B4E758B9877685D966A26ABC', '129D938E2BE521'] # mode-s long
    pms.tell(li[0])
    print("====================================")
    pms.tell(li[0])
    print('icao: ', pms.icao(li[0]))
    # pms.tell(li[1]+li[0])

    # print('icao: ',pms.adsb.callsign(li[0]))

    # print(pms.adsb.position(adsbData))

def getAirPos():
    category = pms.adsb.category("8D4840D6202CC371C32CE0576098")
    callsign = pms.adsb.callsign("8D4840D6202CC371C32CE0576098")

    print('category: ', category)
    print('callsign: ', callsign)

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


def getSufPos():
    msg0 = "8C4841753AAB238733C8CD4020B1"
    msg1 = "8C4841753A8A35323FAEBDAC702D"
    t0 = 1457996410
    t1 = 1457996412
    lat_ref = 51.990
    lon_ref = 4.375
    position = pms.adsb.position(msg0, msg1, t0, t1, lat_ref, lon_ref)
    print("surface pos: ", position)
    return position

def airVelo():
    msgA = "8D485020994409940838175B284F"
    msgB = "8DA05F219B06B6AF189400CBC33F"

    vA = pms.adsb.velocity(msgA)
    vB = pms.adsb.velocity(msgB)
    print("speed,trackAngle(or heading),verticalSpeed,speedType")
    print('vA: ', vA)
    print('vB: ', vB)



# Aircraft operation status


# getSufPos()
# airVelo()
getGeneralInfo()

