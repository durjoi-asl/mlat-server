'''
ADS-B decoding module

For decoding 

'''
import common_tools as tools

## functions to decode TC, df, icao

def df(msg):
    return tools.df(msg)

def icao(msg):
    return tools.icao(msg)

def typecode(msg):
    return tools.typecode(msg)

def position_with_ref(msg, lat_ref, lon_ref):
    """ 
    Decode position with only one message.

    A reference position is required, which can be previously
    calculated location, ground station, or airport location.
    The function works with both airborne and surface position messages.
    The reference position shall be with in 180NM (airborne) or 45NM (surface)
    of the true position.

    Args:
        msg (str): even message (28 hexdigits)
        lat_ref: previous known latitude
        lon_ref: previous known longitude

    Returns:
        (float, float): (latitude, longitude) of the aircraft
    """

    
    pass

print("df: ",df("8D4840D6202CC371C32CE0576098"))