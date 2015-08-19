#!/usr/bin/python
import re
import math
import pandas as pd
from geopy.geocoders import Nominatim
from incf.countryutils import transformations

def iterate(filename):
    df = pd.read_csv(filename, index_col='id')
    df['Continent'] = df.apply(lambda row: find_state(row['location']), axis=1)


def find_state(location):
    if pd.notnull(location):
        location = re.sub(r"(\w)([A-Z])", r"\1 \2", location) #(e.g. BrevigMission => Brevig Mission)
        try:
            geolocator = Nominatim()
            loc = geolocator.geocode(location, language='en')
            country = loc.address.split(',')[-1].strip() # Get the country
            continent = transformations.cn_to_ctn(country) # Get the continent
            return continent
        except:
            return "Not found"
    else:
        print "No location available"
        return "NaN"


iterate(filename='./crystals_metadata.csv')
#iterate(filename='./test.csv')
