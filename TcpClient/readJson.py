import json


def readData():

    try:
        with open("receiversInfo.json") as jsonFile:
            data = json.load(jsonFile)
            # print(data)
    except:
        return None
    
    return data

if __name__ == "__main__":
    data = readData()
    # pprint.pprint(data)

    for item in data:
        print(item)
        keys = item.keys()
        for key in keys:
            print(" ", item[key])