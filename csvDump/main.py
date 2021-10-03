from csvHandler import csvWrite

from DB_handler import findByIcao

import threading
import time

# def storeData(icaoArr):

def save2csv(icao):
    print()
    # work = True
    # timeStart = time.time
    # while work == True:
    print("data collection for ICAO: ", icao)
    while True:
        planeInfo = findByIcao(icao) 
        # print(planeInfo)
        csvWrite(icao+".csv",planeInfo)
        time.sleep(1)

def saveMultiIcao2Csv(icaoList):
    workerList = []

    for icao in icaoList:
        t = threading.Thread(target=save2csv, args=(icao,))
        workerList.append(t)
    
    for worker in workerList:
        worker.start()

    

if __name__ == "__main__":
    # save2csv("800C09")
    saveMultiIcao2Csv(["06A0FE","06A2C7", "702077"])