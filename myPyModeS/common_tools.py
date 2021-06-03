#similar to py_common

import numpy as np

def hex2bin(hexstr) :
    """ hexadecimal string to binary string """
    binData = bin(int(hexstr,16))[2:].zfill(int(len(hexstr)*4))
    return binData

def hex2int(hexstr):
    """ hexadecimal string to integer """
    return int(hexstr)

def bin2int(binstr: str ) -> int:
    """ converts binary string to integer """
    return int(binstr, 2)

def bin2hex(binstr: str) -> str:
    """ converts binary string to hexadecimal string """
    return "{0:X}".format(int(binstr, 2))

from typing import Optional

def df(msg: str ) -> int:
    """ Decode Downlink Format value, bits 1 - 5 """
    dfbin = hex2bin(msg[:2])
    return min(bin2int(dfbin[0:5]), 24)


def icao(msg: str) -> int :
    """
    The ICAO address is located from 9 to 32 bits in binary 
    or 3 to 8 in hexadecimal positions. A unique ICAO address
     is assigned to each Mode S transponder of an aircraft and 
     serves as the unique identifier for each aircraft.
     In principle, this code does not change over the lifetime of 
     the aircraft. However, it is possible to reprogram a transponder 
     so that the messages contain a different address.

     Calculates ICAO address from Mode-S msg

     Only for DF4, DF4, DF20 and DF21 messages.

     Args (msg) : 28 bytes hexadecimal message string

     returns: ICAO address in 6 bytes hexadecimal string
    """
    icao_addr: Optional[str] #returns type is either str or None
    Df = df(msg)

    if Df in (11, 17, 18): # ADS-B message
        icao_addr = msg[2:8]
    elif Df in (0, 4, 5, 16, 20, 21): # this is type Mode-S, not handling Mode-S yet
        icao_addr = "Mode-S message, not handling this yet"
    else:
        addr = None
    
    return icao_addr



def typecode(msg: str) -> Optional[int]: # returns type is None or int
    """
    
    Decodes type-code of ADS-B message

    message structure:
    DF (5)  |  CA (3)  |  ICAO (24)  |         ME (56)        |  PI (24)  |
    (Type code) => (33–37 bin) (8-9 hex) 	(5) 	(TC) 	

    args: msg=> 28 bytes hexadecimal msg string

    returns: type code number of type int
    """

    if df(msg) not in (17, 18):
        return None

    # tc_binary = hex2bin(msg[8:10])
    # tc_int  = bin2int(tc_binary[0:5])
    # tc_integer = bin2int(hex2bin(msg[8:10])[0:5])
    
    tc_bin = hex2bin(msg[8:10])
    tc_integer = bin2int(tc_bin[0:5])
    return tc_integer

def floor(x:float) -> int:
    return int(np.floor(x))

def cprNL(lat: float) -> int:

    """NL() function in CPR decoding."""

    if np.isclose(lat, 0): # if lat is close to 0
        return 59
    elif np.isclose(abs(lat), 87): # if lat is close to 87
        return 2
    elif lat > 87 or lat < -87: 
        return 1

    nz = 15
    a = 1 - np.cos(np.pi / (2 * nz))
    b = np.cos(np.pi / 180 * abs(lat)) ** 2
    nl = 2 * np.pi / (np.arccos(1 - a / b))
    NL = floor(nl)
    return NL

def gray2int(binstr: str):
    """
    convert greycode to binary
    """
    num = bin2int(binstr)
    # ^ caret is for bitwise XOR

    # >> is right shift.
    # x >> y Returns x with the bits shifted
    # to the right by y places.

    num ^= num >> 8
    num ^= num >> 4
    num ^= num >> 2
    num ^= num >> 1

    return num

def gray2alt(binstr: str) -> Optional[int]:
    """
    converts graycode to altitude
    """
    gc500 = binstr[:8]
    n500 = gray2int(gc500)

    # 100foot step must be converted first
    gc100 = binstr[8:]
    n100 = gray2int(gc100)

    if n100 in [0, 5, 6]:
        return None
    
    if n100 == 7:
        n100 = 5
    
    if n500%2: #odd number
        n100 = 6 - n100

    alt = (n500 * 500 + n100 * 100) - 1300
    return alt



def altitude(binstr: str) -> Optional[int]:
    """
    Decode 13 bits altitude code.

    Args: binstr( String ) => 13 bit long binary string

    Returns: ( int ) => the altitude
    """

    alt: Optional[int]

    if len(binstr) != 13 or not set(binstr).issubset(set("01")):
        raise RuntimeError("Input must be 13 bits binary string")
    
    Mbit = binstr[6]
    Qbit = binstr[8]
    
    if bin2int(binstr) == 0:
        # unknown/invalid
        alt = None
    
    elif Mbit == "0": # in feets
        if Qbit == "1": # 35feet increments
            vbin = binstr[:6] + binstr[7] + binstr[9:]
            alt = bin2int(vbin) * 25 - 1000
        if Qbit == "0": # 100feet increments, above 50175 feet
            c1 = binstr[0]
            a1 = binstr[1]
            c2 = binstr[2]
            a2 = binstr[3]
            c4 = binstr[4]
            a4 = binstr[5]
            m = binstr[6]
            b1 = binstr[7]
            q = binstr[8]
            b2 = binstr[9]
            d2 = binstr[10]
            b4 = binstr[11]
            d4 = binstr[12]

            graystr = d2 + d4 + a1 + a4 + b1 + b2 + b4 + c1 + c2 + c4
            alt = gray2alt(graystr)

        if Mbit == "1": # uint in meters
            vbin = binstr[:6] + binstr[7:]
            alt = int(bin2int(vbin)*3.28084) #converting to feet

        return alt

