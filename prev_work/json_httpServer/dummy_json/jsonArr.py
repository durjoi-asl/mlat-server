import json
FILE_DIR = 'jsonArr.json'
def getData(filename=FILE_DIR):
    '''
    returns JSON data from file as python string
    '''
    try:
        print("Trying")
        with open(FILE_DIR) as json_file:
            data = json.load(json_file)
            # print(data)
            # data.append({
            #             "icao": "123dsaf5",
            #             "info": "lorenIsum"
            #             })
            # print(data)
            # print(type(data))
    except:
        print("failed")
        return None
    return data   

def write_json(data, filename=FILE_DIR):
    myData = getData()
    print(myData)
    myData.append(data)
    print(myData)
    with open(filename, 'w') as f:  
        json.dump(myData, f, indent=4)

def firstEntry(data, filename=FILE_DIR):
    myData = []
    print(myData, " insetting as first entry")
    myData.append(data)
    with open(filename, 'w') as f:  
        json.dump(myData, f, indent=4)

tempData = {
        "icao": "123dsaf4",
        "info": "lorenIsum"
        }
# write_json(tempData)
# firstEntry(tempData)

myD = getData()
# keys = []
# for el in enumerate(myD):
#     keys.append(el[1]["icao"])
# print(keys)

def getInfoFromIcao(data, icao):
    for elem in data:
        if elem["icao"] == icao:
            return elem

print(getInfoFromIcao( myD, "123dsaf1")['info'])