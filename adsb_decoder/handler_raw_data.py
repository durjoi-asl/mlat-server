from pyModeS import bin2int, hex2bin



# def update

# def getTC(msg):
#     pass

# def getCallsign(msg):
#     pass

# def getCategory(msg):
#     pass

def getDF(hexMsg):
    '''
    parameter => hexcode message
    returns => Downlink Format(DF)
    '''
    binData = hex2bin(hexMsg)
    return bin2int(binData[0:5])


def getCA(hexMsg):
    '''
    parameter => hexcode message
    returns => Transponder capability(CA)
    '''
    binData = hex2bin(hexMsg)
    return bin2int(binData[5:8])

def getME(hexMsg):
    '''
    parameter => hexcode message
    returns => Message, extended squitter(ME)
    '''
    return hexMsg[8:22]

def getParity(hexMsg):
    '''
    parameter => hexcode message
    returns => Parity/Interrogator ID(PI)
    '''
    return  hexMsg[22:28]

def getStructuredMewssage():
    pass