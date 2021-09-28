from pyModeS import bin2int, hex2bin

'''
Structure of the ME for airborne position
ie ADSBdata[8:22]
+-------+-------+--------+---------+------+------+-------------+-------------+
| TC, 5 | SS, 2 | SAF, 1 | ALT, 12 | T, 1 | F, 1 | LAT-CPR, 17 | LON-CPR, 17 |
+-------+-------+--------+---------+------+------+-------------+-------------+
'''


def getTC(MEbin):
    TC = bin2int(MEbin[0:5])
    print("myTC: ",TC)
    return TC

def getSS(MEbin):
    SS = bin2int(MEbin[5:7])
    print("mySS: ",SS)
    return SS
    
def getSAF(MEbin):
    SAF = bin2int(MEbin[7:8])
    print("mySAF: ",SAF)
    return SAF

def getALT(MEbin):
    ALT = bin2int(MEbin[8:20])
    print("myALT: ",ALT)
    return ALT

def getT(MEbin):
    T = bin2int(MEbin[20:21])
    print("myT: ",T)
    return T

def getF(MEbin):
    F = bin2int(MEbin[21:22])
    print("myF: ",F)
    return F
    
def getLAT_CPR(MEbin):
    lat = bin2int(MEbin[22:39])
    print("myLAT_CPR: ",lat)
    return lat

def getLON_CPR(MEbin):
    print()
    lon = bin2int(MEbin[39:56])
    print("myLON_CPR: ",lon)
    return lon

def getAirbornePosStructure(fullHhexMsg):
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