from django.contrib.gis.geoip2 import GeoIP2


#helper functions

#for location
def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat,lon =g.lat_lon(ip)
    return country, city, lat, lon


def get_center_coordinates(lat_loc, long_loc, lat_des = None, long_des = None):
    '''returns center coordinates between location and distance by taking the
        average of its latitude and longitude 
    '''
    coord = (lat_loc,long_loc)
    if lat_des:
        coord = ((lat_loc+lat_des)/2,(long_loc+long_des)/2)
    return coord

def get_zoom(distance):
    if distance < 100:
        return 12
    elif distance >= 100 and distance < 5000:
        return 7
    else:
        return 2
    