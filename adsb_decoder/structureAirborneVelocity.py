from pyModeS import bin2int, hex2bin

'''
Structure of the ME for airborne-velocity
ie ADSBdata[8:22]
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+
|TC   |ST |IC|IFR|NUC|           |VrSrc|Svr|VR       |RESV|SDif|DAlt   |
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+

example
Message A (sub-type 1):
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+
|TC   |ST |IC|IFR|NUC|           |VrSrc|Svr|VR       |RESV|SDif|DAlt   |
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+
|10011|001|0 |1  |000|10000001001|0    |1  |000001110|00  |0   |0010111|
|     |   |  |   |   |10010100000|     |   |         |    |    |       |
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+
|19   |1  |0 |1  |0  |           |0    |1  |14       |0   |0   |23     |
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+

Message B (sub-type 3):
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+
|TC   |ST |IC|IFR|NUC|           |VrSrc|Svr|VR       |RESV|SDif|DAlt   |
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+
|10011|011|0 |0  |000|11010110110|1    |1  |000100101|00  |0   |0000000|
|     |   |  |   |   |10101111000|     |   |         |    |    |       | 
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+
|5    |3  |0 |0  |0  |           |1    |1  |37       |0   |0   |0      |
+-----+---+--+---+---+-----------+-----+---+---------+----+----+-------+
'''

def getTC(MEbin):
    print(MEbin[0:5])
    TC = bin2int(MEbin[0:5])
    print("myTC: ",TC)
    return TC

def getST(MEbin):
    print(MEbin[5:8])
    ST = bin2int(MEbin[5:8])
    print("myST: ",ST)
    return ST

def getIC(MEbin):
    print(MEbin[8:9])
    IC = bin2int(MEbin[8:9])
    print("myIC: ",IC)
    return IC

def getIFR(MEbin):
    print(MEbin[9:10])
    IFR = bin2int(MEbin[9:10])
    print("myIFR: ",IFR)
    return IFR

def getNUC(MEbin):
    print(MEbin[10:13])
    NUC = bin2int(MEbin[10:13])
    print("myNUC: ",NUC)
    return NUC

def getWHAT(MEbin):
    print(MEbin[13:35])
    WHAT = bin2int(MEbin[13:35])
    print("myWHAT: ",WHAT)
    return WHAT

def getVrSrc(MEbin):
    print(MEbin[35:36])
    VrSrc = bin2int(MEbin[35:36])
    print("myVrSrc: ",VrSrc)
    return VrSrc

def getSvr(MEbin):
    print(MEbin[36:37])
    Svr = bin2int(MEbin[36:37])
    print("mySvr: ",Svr)
    return Svr

def getVR(MEbin):
    print(MEbin[37:46])
    VR = bin2int(MEbin[37:46])
    print("myVR: ",VR)
    return VR

def getRESV(MEbin):
    print(MEbin[46:48])
    RESV = bin2int(MEbin[46:48])
    print("myRESV: ",RESV)
    return RESV

def getSDif(MEbin):
    print(MEbin[48:49])
    SDif = bin2int(MEbin[48:49])
    print("mySDif: ",SDif)
    return SDif

def getDAlt(MEbin):
    print(MEbin[46:48])
    DAlt = bin2int(MEbin[49:56])
    print("myDAlt: ",DAlt)
    return DAlt

def getAirborneVelocityStructure(fullHhexMsg):  
    MEmsg = fullHhexMsg[8:22]
    MEbin = hex2bin(MEmsg)
    return [getTC(MEbin), getST(MEbin), getIC(MEbin), getIFR(MEbin), getNUC(MEbin), getWHAT(MEbin), getVrSrc(MEbin), getSvr(MEbin), getVR(MEbin), getRESV(MEbin), getSDif(MEbin), getDAlt(MEbin)]

if __name__ == "__main__":

    fullHexMsg ="8D485020994409940838175B284F" #type-1
    # fullHexMsg ="8DA05F219B06B6AF189400CBC33F" #type-2
    MEmsg = fullHexMsg[8:22]
    MEbin = hex2bin(MEmsg)

    print(getTC(MEbin))
    getST(MEbin)
    getIC(MEbin)
    getIFR(MEbin)
    getNUC(MEbin)
    getWHAT(MEbin)
    getVrSrc(MEbin)
    getSvr(MEbin)
    getVR(MEbin)
    getRESV(MEbin)
    getSDif(MEbin)
    getDAlt(MEbin)