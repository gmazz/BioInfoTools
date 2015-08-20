#!/usr/bin/python
import re
import pandas as pd
from incf.countryutils import transformations
import requests


def iterate(filename):
    df = pd.read_csv(filename, index_col='id')
    df['continent'] = df.apply(lambda row: find_state(row['location']), axis=1)
    df
    #df.to_csv("models_metadata_II.csv", sep=',')

def find_state(location):
    if pd.notnull(location):
        if len(location) > 2: #Avoid splitting country codes
            location = re.sub(r"(\w)([A-Z])", r"\1 \2", location) #(e.g. BrevigMission => Brevig Mission)
            request = ''
            while not request:
                try:
                    request = geolocalize(location.strip())[0]['address_components'][-1]['short_name']
                    continent = transformations.cca_to_ctn(request)
                    print location, continent
                    return continent
                except:
                    pass
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
