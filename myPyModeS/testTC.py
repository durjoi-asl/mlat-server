from typing import Optional
def df(msg: str ) -> int:
    """ Decode Downlink Format value, bits 1 - 5 """
    dfbin = hex2bin(msg[:2])
    return min(bin2int(dfbin[0:5]), 24)

def hex2bin(hexstr) :
    """ hexadecimal string to binary string """
    binData = bin(int(hexstr,16))[2:].zfill(int(len(hexstr)*4))
    return binData
    # num_of_bits = len(hexstr) * 4
    # binstr = bin(int(hexstr, 16))[2:].zfill(int(num_of_bits))
    # return binstr

def bin2int(binstr: str ) -> int:
    """ converts binary string to integer """
    return int(binstr, 2)


def typecode(msg: str) -> Optional[int]:
    """Type code of ADS-B message

    Args:
        msg (string): 28 bytes hexadecimal message string

    Returns:
        int: type code number
    """
    if df(msg) not in (17, 18):
        return None

    tcbin = hex2bin(msg[8:10])
    return bin2int(tcbin[0:5])

if __name__ == "__main__":
    print(typecode("8C4841753A9A153237AEF0F275BE"))

    