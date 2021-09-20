def checkAircraftType(tc, ca):
    '''
        \nreturns the aircraft type
        \n(tc, ca) => params are typecode and catagory
    '''

    if tc == 1:
        return ["Reserved", 1]

    elif ca == 0:
        return ["No category information", 0]

    elif tc==2 and  ca==1:
        return ["Surface emergency vehicle", 2]

    elif tc==2 and  ca==3:
        return ["Surface service vehicle", 3]

    if tc==2 and  ca in range(4,8):
        return ["Ground obstruction", 4]

    elif tc==3 and  ca==1:
        return ["Glider, sailplane", 5]

    elif tc==3 and  ca==2:
        return ["Lighter-than-air", 6]

    elif tc==3 and  ca==3:
        return ["Parachutist, skydiver", 7]

    if tc==3 and  ca==4:
        return ["Ultralight, hang-glider, paraglider", 8]

    elif tc==3 and  ca==5:
        return ["Reserved", 9]

    elif tc==3 and  ca==6:
        return ["Unmanned aerial vehicle", 10]

    elif tc==3 and  ca==7:
        return ["Space or transatmospheric vehicle", 11]

    if tc==4 and  ca==1:
        return ["Light (less than 7000 kg)", 12]

    elif tc==4 and  ca==2:
        return ["Medium 1 (between 7000 kg and 34000 kg)", 13]

    elif tc==4 and  ca==3:
        return ["Medium 2 (between 34000 kg to 136000 kg)", 14]

    elif tc==4 and  ca==4:
        return ["High vortex aircraft", 15]

    elif tc==4 and  ca==5:
        return ["Heavy (larger than 136000 kg)", 16]

    elif tc==4 and  ca==6:
        return ["High performance (>5 g acceleration) and high speed (>400 kt)", 17]

    elif tc==4 and  ca==7:
        return ["Rotorcraft", 18]
    
    else:
        return ["error error!!", -1]

