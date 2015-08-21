#!/usr/bin/python
import re
import pandas as pd
from incf.countryutils import transformations
import requests
import time


'''Globals'''
location_continent = {}


'''
Reads the initial csv metadata, iterates the 'find_continent' request for each location,
add the result to the newly generated 'continent' column and write the final data_frame to new file
'''
def iterate(filename):
    df = pd.read_csv(filename, index_col='id')
    df['continent'] = df.apply(lambda row: find_continent(row['location']), axis=1)
    df.to_csv("models_metadata_II.csv", sep=',')


'''
Given a location, if the location is non-existent returns Nan, otherwise:
if the location is already present in the location_continent dictionary, returns the continent for that location,
otherwise it firstly query the google geolocation API to extract the country code (two letters), then request the
continent using the obtained country code, by means of the incf.contryutils library.
'''
def find_continent(location):
    if pd.notnull(location):
        if location in location_continent.keys(): # Check if the info are already in the location_continent dict
            continent = location_continent[location]
            print "%s -> %s (from dict)" %(location, continent)
            return continent
        else:
            if len(location) > 2: #Avoid splitting country codes
                location = re.sub(r"(\w)([A-Z])", r"\1 \2", location) #(e.g. BrevigMission => Brevig Mission)
            request = ''
            invalid = ''
            timeout = time.time() + 30 # Setting timeout for API request (in seconds)
            while not request:
                if time.time() > timeout:
                    return invalid
                time.sleep(1)
                try:
                    request = geolocalize(location.strip())[0]['address_components'][-1]['short_name']
                    continent = transformations.cca_to_ctn(request)
                    print "%s -> %s (from API)" %(location, continent)
                    location_continent[location] = continent
                    return continent
                except:
                    invalid = "invalid continent for %s" %location
    else:
        return 'NaN'


'''
Use the google geocode API to get country names from general location names
'''
def geolocalize(address):
   try:
       my_key = 'AIzaSyDg3bQXaesZZbsKCgHjxYVfFouaMC9-QYA' # Google DEV key (https://console.developers.google.com/project/mythic-plexus-101317/apiui/credential/key/0)
       r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?key=%s" %(my_key),
                        params = {"address": address})
       return r.json()['results']
   except:
       return {}


'''
Run the iterate function giving the appropriate csv metadata filename.
Note: the 'location' column need to be present in the csv file.
'''
#iterate(filename='./models_metadata.csv')
#iterate(filename='./crystals_metadata.csv')
#iterate(filename='./test_repeat.csv')
