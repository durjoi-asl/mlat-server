import pyModeS as pms
# import handler_aircraft_identity as hrd
from pyModeS import bin2int, hex2bin

dic = {
    1:"A",
    2:"B",
    3:"C",
    4:"D",
    5:"E",
    6:"F",
    7:"G",
    8:"H",
    9:"I",
    10:"J",
    11:"K",
    12:"L",
    13:"M",
    14:"N",
    15:"O",
    16:"P",
    17:"Q",
    18:"R",
    19:"S",
    20:"T",
    21:"U",
    22:"V",
    23:"W",
    24:"X",
    25:"Y",
    26:"Z",

    32:"␣",

    48:"0",
    49:"1",
    50:"2",
    51:"3",
    52:"4",
    53:"5",
    54:"6",
    55:"7",
    56:"8",
    57:"9",
}


def getTCFromBin(binData):
    binTC = binData[0:5]
    return bin2int(binTC)

def getCAFromBin(binData):
    binCA = binData[5:8]
    return bin2int(binCA)

def getC1FromBin(binData):
    # print("binData: ", binData )
    C1 = binData[8:14]
    # print("C1: ", C1)
    C1int = bin2int(C1)
    # print("C1int: ", C1int)
    # print("C1Char: ", dic[C1int])
    return dic[C1int]
    

def getC2FromBin(binData):
    C2 = binData[14:20]
    C2int = bin2int(C2)
    return dic[C2int]

def getC3FromBin(binData):
    C3 = binData[20:26]
    C3int = bin2int(C3)
    return dic[C3int]
    

def getC4FromBin(binData):
    C4 = binData[26:32]
    C4int = bin2int(C4)
    return dic[C4int]
    
def getC5FromBin(binData):
    C5 = binData[32:38]
    C5int = bin2int(C5)
    return dic[C5int]
    
def getC6FromBin(binData):
    C6 = binData[38:44]
    C6int = bin2int(C6)
    return dic[C6int]
    
def getC7FromBin(binData):
    C7 = binData[44:50]
    C7int = bin2int(C7)
    return dic[C7int]
    

def getC8FromBin(binData):
    C8 = binData[50:56]
    C8int = bin2int(C8)
    return dic[C8int]


def getIdStructureFromHexData(hexData):
    '''
    param => hexData: just the Message(ME) hexcode not the whole hexCode, id hexCode[8:22]
    '''
    print("hexData: ", hexData )
    binData = hex2bin(hexData[8:22])
    print("binData: ", binData)
    return [getTCFromBin(binData), getCAFromBin(binData), getC1FromBin(binData),getC2FromBin(binData),getC3FromBin(binData),getC4FromBin(binData),getC5FromBin(binData),getC6FromBin(binData),getC7FromBin(binData),getC8FromBin(binData)]


if __name__ == "__main__":
    # print("dic: ",dic[22])
    # msg = "8D4840D6202CC371C32CE0576098"
    
    uncutmsg = "8D4840D6202CC371C32CE0576098"
    msg = uncutmsg[8:22]
    print('cut msg: ', msg)
    binMsg = hex2bin(msg)
    # print(getC1FromBin(binMsg))
    print(getIdStructureFromHexData(msg))
    # print("cut msg: ", msg)

    # TC = pms.adsb.typecode(uncutmsg)
    # print("TC pms: ", TC)
    # myTCbin = hrd.hex2bin(msg)
    # myTC = hrd.bin2int(myTCbin[0:5])
    # print("my TC: ", myTC)


    # CA = hrd.getCA(uncutmsg)

    # myBin = hrd.hex2bin(msg)
    # print("binary: ", myBin)