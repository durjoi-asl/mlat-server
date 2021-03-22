import json
import pyModeS as pms
import decrypt

FILE_DIR = "planeDB.json"
REF_LAT = 52.258
REF_LON = 3.918

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
            "identity":[pms.adsb.category(msg),pms.adsb.callsign(msg)],
            "inflight": False,
            "inGround": False,
            "flightInfo":[None,None,None,None],
            "gndInfo": [None,None,None]
        }
    temp[pms.adsb.icao(msg)]=(newItem)

    write_json(temp)
 
def firstEntry(msg):
    temp = {}
    newItem = {
        "identity":[pms.adsb.category(msg),pms.adsb.callsign(msg)],
        "inflight": False,
        "inGround": False,
        "flightInfo":[None,None,None,None],
        "gndInfo": [None,None,None]
    }
    temp[pms.adsb.icao(msg)]=(newItem)
    write_json(temp)


def handleID(msg):
    '''
    handles Idenditiy messages, TypeCode:1-4
    '''

    data = getData()
    
    if data != None or len(data) != 0 :
        keys = data.keys()
        # print("keys: ", keys)
        if pms.adsb.icao(msg) in keys:
            # still check if we're missing some important thing or revise this later
            return
        else:
            createEntry(msg)
    else:
        firstEntry(msg)


def updateAerealPos(msg):
    lt, ln = pms.adsb.airborne_position_with_ref(msg, REF_LAT, REF_LON)
    data = getData()
    temp = {}
    icaoN = pms.adsb.icao(msg)

    if icaoN == None and icaoN not in data.keys():
        return
    else : # if entry exists 
        for key in data.keys():
            if key != icaoN:
                temp[key] = data[key]
            else:
                print('updating aereal data')
                print('eita data: ',data[key]["flightInfo"])
                print('eita data: ',len(data[key]["flightInfo"]))
                newArr = [lt, ln, data[key]["flightInfo"][2], data[key]["flightInfo"][3]]
                # print('eita data: ',data[key]["flightInfo"][3])
                print('eita data: ', newArr)


                item = {
                    "identity":data[key]['identity'],
                    "inflight": True,
                    "inGround": False,
                    # "flightInfo":[lt, ln, data[key]["flightInfo"][2], ["flightInfo"][3]],
                    "flightInfo":newArr,
                    "gndInfo": [None,None,None]
                }
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