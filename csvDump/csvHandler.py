import csv
from os.path import exists


def csvWrite(fileName, newRowArr):
    '''
    takes in fileName, and an array of the ro values to be inserted
    ["icao","identity","inFlight","inGround","flightInfo_lat","flightInfo_long", "flightInfo_velovity_speed", "flightInfo_velovity_magHeading", "flightInfo_velovity_verticalSpeed", "flightInfo_altitude","flight_angle", "gndInfo_lat", "gndInfo_long", "gndInfo_speed", "gndInfo_altitude", "raw_signal_hexcode","raw_signal_timestamp", "raw_decodedHex", "raw_DecodedMsg_msgType", "raw_DecodedMsg_msg"]
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


def csvWrite_rawHex(fileName, newRowArr):
    '''
    takes in fileName, and an array of the ro values to be inserted
    this function if for dumping raw hex message and timestamp
    '''
    fileDir = "csvFiles/"+fileName
    
    if exists(fileDir) == False:
        with open(fileDir, "w") as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(["raw_hexCode", "raw_timeStamp", "ts_seconds", "ts_nanoSeconds", "lat", "long", "type"])

        with open(fileDir, "a") as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(newRowArr)
    else:    
        with open(fileDir, "a") as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(newRowArr)

            
if __name__ == "__main__":
    
    def testCsvWrite_rawHex():
        icao = "raw/testIcao.csv"
        msg = ['8D704011991114AAB0045CE0836A', '2148B807F4DB17']
        for i in range(10):
            csvWrite_rawHex(icao, msg)

    testCsvWrite_rawHex()