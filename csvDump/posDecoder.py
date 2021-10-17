import pyModeS as pms

def getAdsbLatLon_fromRef(msg, refLat, refLong):
    '''
    \n params  => adsb message;
    \n refLat  => reference latitude;
    \n refLong => reference longitude;

    \n returns => calculated position from reference sensor position (lat, long);
    '''
    
    tc = pms.adsb.typecode(msg)
    flag = pms.adsb.oe_flag(msg)
    
    if   flag==0 and tc in range(9,19) or tc in range(20,23)  : # Type Code 9–18 and 20–22 is for aereal position
        
        return [pms.adsb.airborne_position_with_ref(msg, refLat, refLong), 'aereal_position']

    elif tc in range(5,9): # Type Code from 5 to 8 is for surface position

        return [pms.adsb.surface_position_with_ref(msg, refLat, refLong), 'surface_position']
    
    else:
        return False
        

if __name__ == "__main__":
    print(getAdsbLatLon_fromRef("8D40621D58C386435CC412692AD6",22.35443, 91.83391))

    if getAdsbLatLon_fromRef("8D40621D58C382D690C8AC2863A7",22.35443, 91.83391) != False:
        print('proper lat long')
        ltln = getAdsbLatLon_fromRef("8D40621D58C382D690C8AC2863A7",22.35443, 91.83391)
        print('lat: ', ltln[0][0])
        print('lon: ', ltln[0][1])
        print('type: ', ltln[1])
    else:
        print('no can do lat long')
#     getLatLon_fromRef(18)
#     getLatLon_fromRef(20)
#     getLatLon_fromRef(22)