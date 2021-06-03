# ------------------------------------------
#   BDS 0,5
#   ADS-B TC=9-18
#   Airborne position
# ------------------------------------------

import  common_tools

def airborne_position_with_ref(msg, lat_ref, lon_ref):
    """Decode airborne position with only one message,
    knowing reference nearby location, such as previously calculated location,
    ground station, or airport location, etc. The reference position shall
    be with in 180NM of the true position.

    Args:
        msg (str): even message (28 hexdigits)
        lat_ref: previous known latitude
        lon_ref: previous known longitude

    Returns:
        (float, float): (latitude, longitude) of the aircraft
    """
    mb =  common_tools.hex2bin(msg)[32:]

    latcpr = common_tools.bin2int(mb[22:39])/131072
    loncpr = common_tools.bin2int(mb[39:56])/131072

    i = int(mb[21]) #bit 54 determines whether it is an odd or even frame. i=0 if even, i=1 if odd
    dLat = 360/59 if i else 360/60 #if i==odd frame then  dLat = 360/(4Nz-1) else dLat = 360/(4Nz-1)

    j = common_tools.floor(lat_ref/dLat)+common_tools.floor(
        0.5 + ((lat_ref%dLat)/dLat) - latcpr
        )
    lat = dLat * (j+latcpr)

    ni = common_tools.cprNL(lat) - i

    dLon = 360/(max(common_tools.cprNL(lat)-i,1))

    m = common_tools.floor(lon_ref/dLon) + common_tools.floor(
        0.5 + ((lon_ref%dLon)/dLon) - loncpr
        )
    
    lon = dLon*(m+loncpr)

    return round(lat,5), round(lon,5)

def altitude(msg):
    """
    Decode aircraft altitude

    Args:
        msg (str): 28 hexdigits string

    Returns:
        int: altitude in feet
    """
    tc = common_tools.typecode(msg) 

    if tc < 9 or tc==19 or tc > 22:
        raise RuntimeError("%s: Is not an airborne position message" %msg)

    mb = common_tools.hex2bin(msg)[32:] # the altitude message-byte
    altbin = mb[8:20]

    if tc<19: #Barometric altitude
        altcode = altbin[0:6]+"0"+altbin[6:]
        alt = common_tools.altitude[altcode]
    else:
        alt = common_tools.bin2int(altbin) * 3.28084

    return alt


if __name__ == "__main__":

    posMsg="8D40621D58C382D690C8AC2863A7"
    ref = (52.258, 3.918)
    print("airborne position: ")
    print(airborne_position_with_ref(posMsg, ref[0], ref[0]))
    print()

    altMsg = "8D40621D58C382D690C8AC2863A7"
    print("altidude: ",altitude(altMsg))
