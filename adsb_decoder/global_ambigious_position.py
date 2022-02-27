# import math
# from numpy import arccos, cos
# cpr_lat_even = 0b10110101101001000 #93000
# cpr_lon_even = 0b01100100010101100 #51372

# cpr_lat_odd = 0b10010000110101110 #74158
# cpr_lon_odd = 0b01100010000010010 #50194


# lat_cpr_even = (cpr_lat_even)/(2**17)
# lon_cpr_even = (cpr_lon_even)/(2**17)

# lat_cpr_odd = (cpr_lat_odd)/(2**17)
# lon_cpr_odd = (cpr_lon_odd)/(2**17)

# j = math.floor((59*lat_cpr_even) - (60*lat_cpr_odd) + 0.5)

# lat_even = 360/(4*15)*(math.fmod(j, 60) + lat_cpr_even)
# lat_odd = 360/(4*15-1)*(math.fmod(j, 59) + lat_cpr_odd)

# print(lat_even)
# print(lat_odd)

# NL_lat_even = math.floor((2*3.14159)/arccos(1-((1-cos(3.14159/(2*15)))/(cos(3.14159*lat_even/180))**2 )))

# NL_lat_odd = math.floor((2*3.14159)/arccos(1-((1-cos(3.14159/(2*15)))/(cos(3.14159*lat_odd/180))**2 )))

# print(NL_lat_even)
# print(NL_lat_odd)


import pyModeS as pms

msg0 = "8D06A0C258D30048889B0F78BAFD"
msg1 = "126F49986E021E"
t0 = pms.hex2bin("12701F11F6E728")
t1 = pms.hex2bin("12701F11F6E729")

print(pms.adsb.position(msg0, msg1, t0, t1))

import pyModeS as pms

msg = "8D40621D58C382D690C8AC2863A7"
lat_ref = 52.258
lon_ref = 3.918

print(pms.adsb.position_with_ref(msg, lat_ref, lon_ref))