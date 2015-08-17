from geopy.geocoders import Nominatim





def find_state(location):
    geolocator = Nominatim()
    loc = geolocator.geocode(location, language='en')
    state = loc.address.split(',')
    print state

location = "NY"
find_state(location)