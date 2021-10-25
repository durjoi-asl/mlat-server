# ------------------------------------------
#   BDS 0,6
#   ADS-B TC=5-8
#   Surface movment
# ------------------------------------------

# surface position_with_ref, surface_velocity
# haven't implemented surface_position( without reference )

import  common_tools

def surface_position_with_ref(msg, lat_ref, lon_ref):
    """
    Decode surface position with only one message,
    knowing reference nearby location, such as previously calculated location,
    ground station, or airport location, etc. The reference position shall
    be with in 45NM of the true position.

    The surface position message has Type Code from 5 to 8, which also represents 
    the level of uncertainties in the position
    
    And the structure of the surface position message ME field is:
    +-------+--------+------+--------+------+------+-------------+-------------+
    | TC, 5 | MOV, 7 | S, 1 | TRK, 7 | T, 1 | F, 1 | LAT-CPR, 17 | LON-CPR, 17 |
    +-------+--------+------+--------+------+------+-------------+-------------+

    Args:
        msg (str): even message (28 hexdigits)
        lat_ref: previous known latitude
        lon_ref: previous known longitude

    Returns:
        (float, float): (latitude, longitude) of the aircraft
    """

    mb = common_tools.hex2bin(msg)[32:] # 32nd binary bit is the same as 8th hex bit

    cprlat = common_tools.bin2int(mb[22:39]) / 131072 # Lat/2^17
    cprlon = common_tools.bin2int(mb[39:56]) / 131072 # Lon/2^17

    i = int(mb[21]) #bit 54 determines whether it is an odd or even frame. i=0 if even, i=1 if odd

    dLat = 90/59 if i else 90/60 #if i==odd frame then  dLat = 90/(4Nz-1) else dLat = 90/(4Nz-1)

    j = common_tools.floor(lat_ref/dLat) + common_tools.floor(
        0.5 - cprlat + ((lat_ref%dLat)/dLat)
    )
    lat = dLat * (j+cprlat)

    ni = common_tools.cprNL(lat) - i

    dLon = 90/ni if ni>0 else 90

    m = common_tools.floor(lon_ref/dLon) + common_tools.floor(
        0.5 - cprlon + ((lon_ref % dLon))
    )
    lon = dLon * (m + cprlon)

    return round(lat, 5), round(lon, 5)
    
def surface_velocity(msg, source=False):
    """
    Decode surface velocity from a surface position message

    Args:
        msg (str): 28 hexdigits string
        source (boolean): Include direction and vertical rate sources in return. Default to False.
            If set to True, the function will return six value instead of four.

    Returns:
        int, float, int, string, [string], [string]: Four or six parameters, including:
            - Speed (kt)
            - Angle (degree), ground track
            - Vertical rate, always 0
            - Speed type ('GS' for ground speed, 'AS' for airspeed)
            - [Optional] Direction source ('TRUE_NORTH')
            - [Optional] Vertical rate source (None)
    """
    print('TC: ', common_tools.typecode(msg))
    if common_tools.typecode(msg) < 5 or common_tools.typecode(msg) > 8:
        raise RuntimeError("%s: Not a surface message, typecode should be 5<TC<8 " %msg)

    mb = common_tools.hex2bin(msg)[32:] # message-byte 32nd binary bit is the same as 8th hex bit

    # ground track
    trk_status = int(mb[12])
    if trk_status == 1:
        trk = common_tools.bin2int(mb[13:20]) * 360/128
        trk = round(trk, 1)
    else:
        trk = None

    # ground movement / speed
    mov = common_tools.bin2int(mb[5:12])

    if mov == 0 or mov > 124:
        spd = None
    elif mov == 1:
        spd = 0
    elif mov == 124:
        spd = 175
    else:
        mov_lb = [2, 9, 13, 39, 94, 109, 124]
        kts_lb = [0.125, 1, 2, 15, 70, 100, 175]
        step = [0.125, 0.25, 0.5, 1, 2, 5]
        i = next(m[0] for m in enumerate(mov_lb) if m[1]>mov)
        spd = kts_lb[i-1] + (mov - mov_lb[i-1]) * step[i-1]
    if source:
        return spd, trk, 0, "GS", "True_North", None
    else:
        return spd, trk, 0, "GS"



if __name__ == "__main__":
    
    # surface position with reference
    print("surfeace_position_with_ref: ",surface_position_with_ref("8C4841753A9A153237AEF0F275BE", 51.990, 4.375))

    # surface velocity
    print("surface velocity: ", surface_velocity("8C4841753A9A153237AEF0F275BE"))

