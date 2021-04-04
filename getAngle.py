import math as Math
def angleFromCoordinate(lat1,lon1,lat2,lon2) :

    # angle in degrees
    angleDeg = Math.atan2(lon2 - lon1, lat2 - lat1) * 180 / Math.pi
    
    print(360+angleDeg)
    
    return angleDeg