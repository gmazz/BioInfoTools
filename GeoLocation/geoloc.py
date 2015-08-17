import re
import pandas as pd
from geopy.geocoders import Nominatim


def iterate(filename):
    df = pd.read_csv(filename, index_col='id')
    df['State'] = df.apply(lambda row: find_state(row['location']), axis=1)
    print df

def find_state(location):
    location = re.sub(r"(\w)([A-Z])", r"\1 \2", location) #(e.g. BrevigMission => Brevig Mission)
    try:
        geolocator = Nominatim()
        loc = geolocator.geocode(location, language='en')
        state = loc.address.split(',')[-1]
        return state
    except:
        return "Not found"


#iterate(filename='./crystals_metadata.csv')
iterate(filename='./test.csv')


#find_state(raw_locations)