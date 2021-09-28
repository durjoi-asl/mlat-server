from pyModeS import bin2int, hex2bin

'''
Structure of the ME for surface(ground) position
ie ADSBdata[8:22]
+-------+--------+------+--------+------+------+-------------+-------------+
| TC, 5 | MOV, 7 | S, 1 | TRK, 7 | T, 1 | F, 1 | LAT-CPR, 17 | LON-CPR, 17 |
+-------+--------+------+--------+------+------+-------------+-------------+
'''

def getTC(MEbin):
    # print(MEbin[0:5])
    TC = bin2int(MEbin[0:5])
    # print("myTC: ",TC)
    return TC

def getMOV(MEbin):
    # print(MEbin[5:12])
    MOV = bin2int(MEbin[5:12])
    # print("myMOV: ",MOV)
    return MOV

def getS(MEbin):
    # print(MEbin[12:13])
    S = bin2int(MEbin[12:13])
    # print("myS: ",S)
    return S

def getTRK(MEbin):
    # print(MEbin[13:20])
    TRK = bin2int(MEbin[13:20])
    # print("myTRK: ",TRK)
    return TRK

def getT(MEbin):
    # print(MEbin[20:21])
    T = bin2int(MEbin[20:21])
    # print("myT: ",T)
    return T

def getF(MEbin):
    # print(MEbin[21:22])
    F = bin2int(MEbin[21:22])
    # print("myF: ",F)
    return F

def getLAT_CPR(MEbin):
    # print(MEbin[22:39])
    lat = bin2int(MEbin[22:39])
    # print("LAT_CPR: ",lat)
    return lat

def getLON_CPR(MEbin):
    # print(MEbin[39:56])
    lon = bin2int(MEbin[39:56])
    # print("myLON_CPR: ",lon)
    return lon

def getSurfacePosStructure(fullHhexMsg):
    MEmsg = fullHhexMsg[8:22]
    MEbin = hex2bin(MEmsg)
    return [getTC(MEbin), getMOV(MEbin), getS(MEbin), getTRK(MEbin), getT(MEbin), getF(MEbin), getLAT_CPR(MEbin), getLON_CPR(MEbin)]


if __name__ == "__main__":
    # fullHexMsg = "8C4841753AAB238733C8CD4020B1"
    fullHexMsg ="8C4841753A9A153237AEF0F275BE"
    MEmsg = fullHexMsg[8:22]
    MEbin = hex2bin(MEmsg)

    getTC(MEbin)
    getMOV(MEbin)
    getS(MEbin)
    getTRK(MEbin)
    getT(MEbin)
    getF(MEbin)
    getLAT_CPR(MEbin)
    getLON_CPR(MEbin)