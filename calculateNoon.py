
# # next where are Tx, Rx, when is your path on the dayside, how to throw away the night. 
# import geographiclib
# import geopy
# import haversine
# import ephem
# import astral # package for calculating sunrise/ sunset
# import skyline
import numpy as np






#https://latitude.to/articles-by-country/us/united-states/38984/vlf-transmitter-cutler
# NAA: Cutler Latitude: 44° 38' 28.20" N
#Longitude: -67° 16' 31.11" W
# time: UCT-4 (EDT Eastern Daylight North America)

# Empfänger Ny Alesund 78° 55′ N, 11° 56′ O 
# X = 1202434.158 m	
# Y = 252632.23   m	
# Z = 6237772.523 m

# http://geomidpoint.com/
# Center of minimum distance:
# Latitude: 65.397622
# Longitude: -53.107806

# calculate sunrise and sunset with formula from Benjamin 
def only_daytime(noon_value, midpoint):
    # calculate the noon
    noon = -53.107806*12/(-180)+12
    # calculate sunrise and sunset times
    # midpoint = [65.397622,-53.107806]
    
    # # sunrise at Cutler
    # sunrise_coordinates = [44.64503, -67.28315]
    # # Sunset at Ny Alesund
    # sunset_coordinates = [78.929479, 11.897683]
    
    #number of hours that the "noon" at midpoint is shifted in UCT
    noon_shift = midpoint[1]*12/-180 
    
    #Earths orbit around the sun in degree (=the year)
    angle_of_earth = np.linspace(0,2*np.pi,365,endpoint=False) 
    
    # the declination of sunlight at the equator
    declination_at_eq = np.arcsin(-np.sin(23.5*np.pi/180)*np.cos(angle_of_earth)) 
    
    H = -np.tan(midpoint[0]*np.pi/180)*np.tan(declination_at_eq)
    # cut vlaues below -1 and over 1
    H = np.where(H<-1,-1,H)
    H = np.where(H>1,1,H)
    # calculate half day out of H -> hours of sun at the day (local)
    half_day = np.arccos(H)
    # the half-day length = the amount of hourses that is sunlit
    half_day = half_day*24/np.pi
    
     
    # 12 is höchster sonnenstand
    sunrise_local = (noon_value - half_day/2)%24
    sunset_local  = (noon_value + half_day/2)%24
     
    # print('sunrise:',len(sunrise_uct), sunrise_uct[0:5],'\nsunset:',len(sunset_uct), sunset_uct[0:5])
    return sunrise_local, sunset_local, noon_shift
    
