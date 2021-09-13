def checkAircraftType(tc, ca):
    '''
        \nreturns the aircraft type
        \n(tc, ca) => params are typecode and catagory
    '''

    if tc == 1:
        return "Reserved"

    elif ca == 0:
        return "No category information"

    elif tc==2 and  ca==1:
        return "Surface emergency vehicle"

    elif tc==2 and  ca==3:
        return "Surface service vehicle"

    if tc==2 and  ca in range(4,8):
        return "Ground obstruction"

    elif tc==3 and  ca==1:
        return "Glider, sailplane"

    elif tc==3 and  ca==2:
        return "Lighter-than-air"

    elif tc==3 and  ca==3:
        return "Parachutist, skydiver"

    if tc==3 and  ca==4:
        return "Ultralight, hang-glider, paraglider"

    elif tc==3 and  ca==5:
        return "Reserved"

    elif tc==3 and  ca==6:
        return "Unmanned aerial vehicle"

    elif tc==3 and  ca==7:
        return "Space or transatmospheric vehicle"

    if tc==4 and  ca==1:
        return "Light (less than 7000 kg)"

    elif tc==4 and  ca==2:
        return "Medium 1 (between 7000 kg and 34000 kg)"

    elif tc==4 and  ca==3:
        return "Medium 2 (between 34000 kg to 136000 kg)"

    elif tc==4 and  ca==4:
        return "High vortex aircraft"

    elif tc==4 and  ca==5:
        return "Heavy (larger than 136000 kg)"

    elif tc==4 and  ca==6:
        return "High performance (>5 g acceleration) and high speed (>400 kt)"

    elif tc==4 and  ca==7:
        return "Rotorcraft"
    
    else:
        return "error error!!"

