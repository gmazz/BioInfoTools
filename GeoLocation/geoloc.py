#!/usr/bin/python
import re
import pandas as pd
from geopy.geocoders import Nominatim
from incf.countryutils import transformations
import requests


def iterate(filename):
    df = pd.read_csv(filename, index_col='id')
    df['continent'] = df.apply(lambda row: find_state(row['location']), axis=1)
    print df
    #df.to_csv("models_metadata_II.csv", sep=',')

def find_state(location):
    if pd.notnull(location):
        try:
            location = re.sub(r"(\w)([A-Z])", r"\1 \2", location) #(e.g. BrevigMission => Brevig Mission)
           # geolocator = Nominatim()
           # loc = geolocator.geocode(location, language='en')
           # country = loc.address.split(',')[-1].strip() # Get the country
            country_code = geolocalize(location)[0]['address_components'][-1]['short_name']
            #country_code = geolocalize(country)[0]['address_components'][0]['short_name']
            continent = transformations.cca_to_ctn(country_code)
            #print country_code, continent
            return continent
        except:
            print "Problem getting country"
            return 'NaN'
    else:
        return 'NaN'


def geolocalize(address):
   try:
       r = requests.get("https://maps.googleapis.com/maps/api/geocode/json",
                        params={"address": address})
       return r.json()['results']
   except:
       return {}

#iterate(filename='./models_metadata.csv')
iterate(filename='./test.csv')
