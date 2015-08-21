#!/usr/bin/python
import re
import pandas as pd
from incf.countryutils import transformations
import requests
import time


def iterate(filename):
    df = pd.read_csv(filename, index_col='id')
    df['continent'] = df.apply(lambda row: find_state(row['location']), axis=1)
    df.to_csv("models_metadata_II.csv", sep=',')

def find_state(location):
    if pd.notnull(location):
        if len(location) > 2: #Avoid splitting country codes
            location = re.sub(r"(\w)([A-Z])", r"\1 \2", location) #(e.g. BrevigMission => Brevig Mission)
            request = ''
            timeout = time.time() + 30
            while not request:
                if time.time() > timeout:
                    break
                time.sleep(1)
                try:
                    request = geolocalize(location.strip())[0]['address_components'][-1]['short_name']
                    continent = transformations.cca_to_ctn(request)
                    print location, continent
                    return continent
                except:
                    invalid = "invalid continent for %s" %location
    else:
        return 'NaN'


def geolocalize(address):
   try:
       r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDg3bQXaesZZbsKCgHjxYVfFouaMC9-QYA",
                        params = {"address": address})
       return r.json()['results']
   except:
       return {}

#iterate(filename='./models_metadata.csv')
iterate(filename='./test.csv')
