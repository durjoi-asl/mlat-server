#similar to py_common

def hex2bin(hexstr) :
    """ hexadecimal string to binary string """
    binData = bin(int(hexstr,16))[2:].zfill(int(len(hexstr)))
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
    tc_integer = bin2int(hex2bin(msg[8:10])[0:5])

    return tc_integer

