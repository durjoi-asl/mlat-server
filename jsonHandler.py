import json
import pyModeS as pms
import decrypt
import getAngle

FILE_DIR = "planeDB.json"
REF_LAT = 23.83588
REF_LON = 90.41611

def getData(filename=FILE_DIR):
    '''
    returns JSON data from file as python string
    '''
    try:
        with open(FILE_DIR) as json_file:
            data = json.load(json_file)
    except:
        return None
    return data                    

def checkPlane(icaoId):
    '''
    checks if plane exists in DB
    '''
    pass

def createEntry(msg):
    '''
    creates new entry for new icao address found
    '''

    temp = getData()
    newItem = {
            "identity":{
                "category":pms.adsb.category(msg),
                "callsign":pms.adsb.callsign(msg)
                },
            "inflight": False,
            "inGround": False,
            "flightInfo": {
                "lat":None,
                "long": None,
                "speed": None,
                "altitude": None,
                "prevPos": None,
                "angle": 0

            },
            "gndInfo": [None,None,None]
        }
    temp[pms.adsb.icao(msg)]=(newItem)

    write_json(temp)
 
def firstEntry(msg):
    '''
    creates new entry for new icao address found
    '''
    temp = {}
    newItem = {
        "identity":{
                "category":pms.adsb.category(msg),
                "callsign":pms.adsb.callsign(msg)
                },
        "inflight": False,
        "inGround": False,
        "flightInfo": {
                "lat":None,
                "long": None,
                "speed": None,
                "altitude": None,
                "prevPos": None,
                "angle": 0
        },
        "gndInfo": [None,None,None]
    }
    temp[pms.adsb.icao(msg)]=(newItem)
    write_json(temp)


def handleID(msg):
    '''
    handles Idenditiy messages, TypeCode:1-4
    '''

    data = getData()
    if data != None : #  just checking if there aren't any previous data  [or len(data) != 0 removed this as if data == null len check is not applicable]
        keys = data.keys()
        # print("keys: ", keys)
        if pms.adsb.icao(msg) in keys:
            # if key exists don't make and entry
            # still check if we're missing some important thing or revise this later
            return
        else:
            createEntry(msg)
    else: # if data == None ie there is no entry in DB then just do firstEntry, also firstEntry and createEntry are different functions
        firstEntry(msg)


def updateAerealPos(msg):
    lt, ln = pms.adsb.airborne_position_with_ref(msg, REF_LAT, REF_LON)
    data = getData()
    temp = {}
    icaoN = pms.adsb.icao(msg)
    print("#################################[data: ]", data)
    if icaoN == None or data == None or icaoN not in data.keys() or data == None:
        return
    else : # if entry exists 
        for key in data.keys():
            if key != icaoN:
                temp[key] = data[key]
            else:
                print('updating aereal data')
                print('eita data: ',data[key]["flightInfo"])
                print('eita data: ',len(data[key]["flightInfo"]))
                # newArr = [lt, ln, data[key]["flightInfo"][2], data[key]["flightInfo"][3]]
                # print('eita data: ',data[key]["flightInfo"][3])
                # print('eita data: ', newArr)


                item = {
                    "identity":data[key]['identity'],
                    "inflight": True,
                    "inGround": False,
                    # "flightInfo":[lt, ln, data[key]["flightInfo"][2], ["flightInfo"][3]],
                    "flightInfo":{
                        "lat":lt,
                        "long": ln,
                        "speed": data[key]["flightInfo"]["speed"],
                        "altitude": data[key]["flightInfo"]["altitude"],
                        "prevPos": {
                            "lat": data[key]["flightInfo"]["lat"],
                            "long": data[key]["flightInfo"]["long"],
                            }
                        # "angle": getAngle.angleFromCoordinate(data[key]["flightInfo"]["lat"],data[key]["flightInfo"]["long"], lt, ln)
                    },
                    "gndInfo": [None,None,None]
                }
                if data[key]["flightInfo"]["lat"] != None: # lat long info not available
                    
                    newAngle = getAngle.angleFromCoordinate(data[key]["flightInfo"]["lat"],data[key]["flightInfo"]["long"], lt, ln)
                    print(data)
                    prevAngle = data[key]["flightInfo"]["angle"]

                    if data[key]["flightInfo"]["prevPos"] != None:
                        if abs(data[key]["flightInfo"]["angle"]-newAngle) > 15:
                            item["flightInfo"]["angle"] = newAngle
                        else:
                            item["flightInfo"]["angle"] = prevAngle
                    else:
                        item["flightInfo"]["angle"] = 0
                else:
                    item["flightInfo"]["angle"] = 0
                    
                temp[key] = item
        write_json(temp)
    # else: # if no entry exists do nothing
    #     return



    print("=================================================position:  ", (lt, ln))

def updateGndInfo():

    pass

def delPlaneInfo():

    pass

def delFlightInfo():

    pass


def write_json(data, filename=FILE_DIR):
    with open(filename, 'w') as f:  
        json.dump(data, f, indent=4)


def handle_data(msg):
    msgTC = pms.adsb.typecode(msg)
    # print('message TC: ', msgTC)
    # print('------------------found position message--------------------')
    if msgTC in range(9,19) or msgTC in range(20,23): #checking if TC == local aereal position
        
        updateAerealPos(msg)
        # print('air position: ', decrypt.getAirbornePos(msg[0]))
    elif msgTC in  range(1,5): #identity typecode
        handleID(msg)
    elif msgTC in range(5,9): #ground position
        print('ground position')
    elif msgTC == 19: #airborne velocity
        print('airborne velocity')


if __name__ == "__main__":
    # write_test()
    # edit_data()
    
    testMsg = '8D7100B3254D6073D78D200D20EE'
    handleID(testMsg)