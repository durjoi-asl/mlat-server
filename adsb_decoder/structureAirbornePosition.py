from pyModeS import bin2int, hex2bin

'''
Structure of the ME for airborne position
ie ADSBdata[8:22]
+-------+-------+--------+---------+------+------+-------------+-------------+
| TC, 5 | SS, 2 | SAF, 1 | ALT, 12 | T, 1 | F, 1 | LAT-CPR, 17 | LON-CPR, 17 |
+-------+-------+--------+---------+------+------+-------------+-------------+
'''


def getTC(MEbin):
    '''
    param =>  binary ME message
    returns => returns int TC; ie. ME[0:5]
    '''
    TC = bin2int(MEbin[0:5])
    return TC

def getSS(MEbin):
    '''
    param => binary ME message
    returns => returns int SS; ie. ME[5:7]
    '''
    SS = bin2int(MEbin[5:7])
    return SS
    
def getSAF(MEbin):
    '''
    param =>  binary ME message
    returns => returns int SAF; ie. ME[7:8]
    '''
    SAF = bin2int(MEbin[7:8])
    return SAF

def getALT(MEbin):
    '''
    param =>  binary ME message
    returns => returns int ALT; ie. ME[8:20]
    '''
    ALT = bin2int(MEbin[8:20])
    return ALT

def getT(MEbin):
    '''
    param =>  binary ME message
    returns => returns int T; ie. ME[20:21]
    '''
    T = bin2int(MEbin[20:21])
    return T

def getF(MEbin):
    '''
    param =>  binary ME message
    returns => returns int F(Flag); ie. ME[21:22]
    '''
    F = bin2int(MEbin[21:22])
    return F
    
def getLAT_CPR(MEbin):
    '''
    param =>  binary ME message
    returns => returns int LAT-CPR; ie. ME[22:39]
    '''
    lat = bin2int(MEbin[22:39])
    return lat

def getLON_CPR(MEbin):
    '''
    param => get binary ME message
    returns => returns int LON-CPE; ie. ME[39:56]
    '''
    # print()
    lon = bin2int(MEbin[39:56])
    # print("myLON_CPR: ",lon)
    return lon

def getAirbornePosStructure(fullHhexMsg):
    '''
    param => get hexcode
    returns => returns [ TC, SS, SAF, ALT, T, F, LAT-CPR, LON-CPR ]
    '''
    MEmsg = fullHhexMsg[8:22]
    MEbin = hex2bin(MEmsg)
    return [getTC(MEbin), getSS(MEbin), getSAF(MEbin), getALT(MEbin), getT(MEbin), getF(MEbin), getLAT_CPR(MEbin), getLON_CPR(MEbin)]

if __name__ == "__main__":

    fullHhexMsg =  "8D40621D58C382D690C8AC2863A7"
    MEmsg = fullHhexMsg[8:22]
    MEbin = hex2bin(MEmsg)

    # getAirbornePosStructure(fullHhexMsg)

    getTC(MEbin)
    getSS(MEbin)
    getSAF(MEbin)
    getALT(MEbin)
    getT(MEbin)
    getF(MEbin)
    getLAT_CPR(MEbin)
    getLON_CPR(MEbin)