from pyModeS import hex2bin, hex2int
import datetime

hours = datetime.timedelta(hours=6)
def decodeTimeStampSeconds(tsHex):
    '''
    \n params  => takes hex time stamp;
    \n returns => the decoded Seconds in Hr:Min:Sec format
    '''

    tsBin = hex2bin(tsHex.lower()) #converting timestamp hex to timestamp binary
    tsBinSec = tsBin[0:18] #taking first 18 binary bits for seconds
    tsNow = datetime.timedelta(seconds=int(tsBinSec,2)) + hours #converting time to GMT, then adding 6hours for BST(Bangladesh Standard Time)
    return tsNow

def decodeTimeStampNanoSeconds(tsHex):
    '''
    params  => takes hex time stamp 
    returns => the decoded NanoSeconds 
    '''
    tsBin = hex2bin(tsHex.lower()) #converting timestamp hex to timestamp binary
    tsBinNanoSec = tsBin[18:48] #taking lower 30 binary bits for nano-seconds
    nanoSeconds = int(tsBinNanoSec,2)
    return nanoSeconds

def decodeTimeStampSeondsAndNanoSeconds(tsHex):
    '''
    params  => takes hex time stamp 
    returns => the decoded Seconds in Hr:Min:Sec format and Nanoseconds in an array [ Seconds, nanoseconds]
    '''
    tsBin = hex2bin(tsHex.lower()) #converting timestamp hex to timestamp binary
    tsBinSec = tsBin[0:18] #taking first 18 binary bits for seconds
    tsBinNanoSec = tsBin[18:48] #taking first 18 binary bits

    tsNow = datetime.timedelta(seconds=int(tsBinSec,2)) + hours #converting time to GMT, then adding 6hours for BST(Bangladesh Standard Time)
    nanoSeconds = int(tsBinNanoSec,2) #
    return [tsNow, nanoSeconds]
    # return tsNow

if __name__ == "__main__":
    '''
    for testing
    '''
    tsHex = '13EC2775CFC83A'
    hex2 =  '244bbb9ac9f0'
    tsNow = decodeTimeStampSeconds(tsHex)
    print('timeNow Seconds: ',tsNow)
    print('type: ' ,type(tsNow))

    nanoSec = decodeTimeStampNanoSeconds('244bbb9ac9f0')

    csvData = '11B75D27EBDA17'
    csvData1 = decodeTimeStampSeondsAndNanoSeconds('12C81C4F38E13C')
    print('csvData1: ',csvData1[0], csvData1[1])