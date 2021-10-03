import csv
from os.path import exists


def csvWrite(fileName, newRowArr):
    '''
    takes in fileName, and an array of the ro values to be inserted
    '''
    fileDir = "csvFiles/"+fileName
    
    if exists(fileDir) == False:
        with open(fileDir, "w") as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(["icao","identity","inFlight","inGround","flightInfo_lat","flightInfo_long", "flightInfo_velovity_speed", "flightInfo_velovity_magHeading", "flightInfo_velovity_verticalSpeed", "flightInfo_altitude","flight_angle", "gndInfo_lat", "gndInfo_long", "gndInfo_speed", "gndInfo_altitude", "raw_signal_hexcode","raw_signal_timestamp", "raw_decodedHex", "raw_DecodedMsg_msgType", "raw_DecodedMsg_msg"])

        with open(fileDir, "a") as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(newRowArr)
    else:    
        with open(fileDir, "a") as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(newRowArr)
        
