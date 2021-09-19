import json

def getData(filename='planeDB.json'):

    pass                    

def checkPlane(icaoId):
    '''
    checks if plane exists in DB
    '''
    pass

def createEntry():

    with open('planeDB.json') as json_file:
        data = json.load(json_file)
        temp = data["names"]
        y = {'firstname':'shady', 'age':69}
        temp.append(y)

    write_json(data)
    

def updateFlightInfo():

    pass

def updateGndInfo():

    pass

def delPlaneInfo():

    pass

def delFlightInfo():

    pass


def write_json(data, filename='planeDB.json'):
    with open(filename, 'w') as f:  
        json.dump(data, f, indent=4)

def write_test():
    with open('planeDB.json') as json_file:
        data = json.load(json_file)
        temp = data["names"]
        y = {'firstname':'shady', 'age':69}
        temp.append(y)

    write_json(data)

def edit_data( filename='planeDB.json'):
    with open(filename) as json_file:
        data = json.load(json_file)
        newData = {}

        name = input("choose name to edit: ")
        newAge = input("choose new age for selected name: ")

        # keys = data.keys()
        # for key in keys:
        #     firstData = data[key]

        newData['icao1'] = []
        # print(newData['icao1'][0])
        for item in data['icao1']:
            if item["firstname"] == name:
                newItem = {
                    "firstname": name,
                    "age": newAge
                }
                newData['icao1'].append(newItem)
            else:
                newData['icao1'].append(item)

        write_json(newData)
        



if __name__ == "__main__":
    # write_test()
    edit_data()