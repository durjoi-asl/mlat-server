from math import pow

def hexDigit2dec(hexDigit):
    '''
    converts a hexadecimal digit string to a decimal digit string
    arguement => hexDigit string
    returns   => decimal conversion of that hex digit
    '''
    # hexDigit = hexDigit.lower()
    # print("hexDigit in digit to dec: ",hexDigit)
    # print('type: ', type(hexDigit))
    # print('len: ', len(hexDigit))
    hexDic = {
        "0":"0",
        "1":"1",
        "2":"2",
        "3":"3",
        "4":"4",
        "5":"5",
        "6":"6",
        "7":"7",
        "8":"8",
        "9":"9",
        "a":"10",
        "b":"11",
        "c":"12",
        "d":"13",
        "e":"14",
        "f":"15",
    }
        
    if hexDigit in hexDic.keys():
        print("converting hex to dec: ", hexDic[hexDigit])
        return hexDic[hexDigit]
    
    else:
        return "X[{}]".format(hexDigit)

def hex2dec(hexNum):
    '''
    converts a hexadecimal number string to a decimal number string
    '''

    decNum = ""
    # print("hexNum: ", hexNum)
    for hexDigit in hexNum:
        # print("hexDigit: ", hexDigit)
        decNum = decNum + hexDigit2dec(hexDigit)+" "
        # hexDigit2dec(hexDigit)
    return decNum

def hex2DecArr(hexNum):
    decArr = []
    for hexDigit in hexNum:
        # print("hexDigit: ", hexDigit)
        decArr.append( hexDigit2dec(hexDigit))
        # hexDigit2dec(hexDigit)
    return decArr

def decodeTs(hexTs):
    powerSec = [7,6,5,4,3,2,1,0]
    powerNsec = [-1,-2,-3,-4]

    hexTs = hexTs[0:12]
    seconds = hexTs[0:8]
    nanoSeconds = hexTs[8:]

    secDecArr = hex2DecArr(seconds)
    nanoSecDecArr = hex2DecArr(nanoSeconds)

    print('seconds: ', secDecArr)
    print('nano: ', nanoSecDecArr)

    for index, item in enumerate(secDecArr):
        secDecArr[index] = int(item)*pow(16, powerSec[index])
    
    for index, item in enumerate(nanoSecDecArr):
        nanoSecDecArr[index] = int(item)*pow(16, powerNsec[index])

    totSec = 0
    totNanoSec = 0
    
    print()
    print('seconds: ', secDecArr)
    print('nano: ', nanoSecDecArr)
    print()

    for i in secDecArr:
        totSec += i
    for i in nanoSecDecArr:
        totNanoSec += i
    
    print('totSec: ', totSec)
    print('TotNanoSec: ', totNanoSec)

# ok = decodeTs('0ff3511f4bb72d')
ok = decodeTs('55f515fffc1b7700') #from book

# ok = decodeTs('10190D0C03262E')


# ts = "55f515fffc1b7700"
# time_msg = ts[0:12]

# time_msg1 = time_msg[0:8]  
# time_msg2 = time_msg[8:]


# print("time_msg: ",time_msg)
# print("time_msg1: ",time_msg1)
# print('time_msg1: ', time_msg2)

# # print(hexDigit2dec('Af'))

# decArr = hex2DecArr("55f515f")
# print(decArr)
# decArr2 = hex2DecArr(time_msg1)
# print(decArr2)
# hex2dec("55f515f")