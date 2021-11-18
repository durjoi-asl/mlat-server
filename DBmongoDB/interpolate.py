import math as Math
from numpy import arctan2,sin,cos,degrees,tan
from DB_Connection import getADSBcollection, getFlightHistoryCollection
import datetime
import time

def angleFromCoordinate(lat1,lon1,lat2,lon2) :
    '''
        returns angles in degress between two (lat,long) coordinates
        /n (old_lat, old_lon, new_lat, new_lon)
    '''
    
    dL =Math.radians(lon2-lon1)
    lat1 = Math.radians(lat1)
    lat2 = Math.radians(lat2)
    lon1 = Math.radians(lon1)
    lon2 = Math.radians(lon2)
    X = cos(lat2)*sin(dL)
    Y = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dL)
    bearing = arctan2(X,Y)
    angleDeg = degrees(bearing)
    return angleDeg

def interpolate(lat,long, angle): # X=long Y=lat
    '''
        interpolates aircraft position in the direction of its track(TRK)/Angle
    '''
    dX = 0.0001 # quadrant 1 and 4
    # if angle>=90 and angle<=180 or angle<=-180 and angle>=-270 or angle>=180 and angle<=270 or angle<=-90 and angle>=-180: # quadrant 2 and 3
    #     dX = -0.0001

    if angle < 0 and angle > -180:
        dX = -0.0001

    #Convert angle into quadrant friendly
    if angle>0 and angle<=90: #first quadrant
        angle = 90-angle
    elif angle > 90 and angle <= 180: #fourth quadrant
        angle = -(angle-90)
    elif angle < 0 and angle >= -90: #second quadrant
        angle = 90-angle
    else: #third quadrant
        angle = 90-angle

    print("dX: ",dX)
    X1 = long
    Y1 = lat
    Y = tan(angle*Math.pi/180)*dX + Y1 # angle*Math.pi/180 converts degrees to rads
    X = X1 + dX
    # return(round(Y,5), round(X,5))
    return(round(Y,5), round(X,5))

def run():
    
    TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"
    adsbCollection = getADSBcollection()
    while True:
        cursor = adsbCollection.find()
        list_cur = list(cursor)
        data = list_cur
        
        for planeData in data:
            print('reading planeData in Data for interpolation')
            timeStamp = datetime.datetime.strptime(planeData["last_updated"], TIME_FORMAT)
            time_now = datetime.datetime.now()
            diff = (time_now-timeStamp).total_seconds()
            data_icao = planeData['icao']

            lat = planeData["flightInfo"]["lat"]
            long = planeData["flightInfo"]["long"]
            angle = planeData["flightInfo"]["angle"]
            print('difference in time: ', diff)
            if diff > 120 and lat!=None:
                print("MUST INTERPOLATE: ", planeData["icao"])
                
                newLat, newLong = interpolate(lat, long, angle)
                adsbCollection.find_one_and_update({"icao":data_icao},{'$set':{"flightInfo.lat":newLat, "flightInfo.long":newLong}})
            else:
                print("No need to interpolate: ", planeData['icao'])
        time.sleep(5)


if __name__ == "__main__":
    print('running tests for interpolation')
    print()

    print('zone 1')
    coor = interpolate(1,1,45)
    print('coor', coor)
    print()

    print('zone 2') # y=-x
    coor = interpolate(0,0,135)
    print('coor', coor)
    print()

    print('zone 3')
    coor = interpolate(1,-1,-45)
    print('coor', coor)
    print()

    print('zone 4') # y=-x
    coor = interpolate(1,-1,-45)
    print('coor', coor)
    print()

    run()