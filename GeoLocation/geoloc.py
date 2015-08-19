#!/usr/bin/python
import re
import math
import pandas as pd
from geopy.geocoders import Nominatim
from incf.countryutils import transformations

def iterate(filename):
    df = pd.read_csv(filename, index_col='id')
    df['Continent'] = df.apply(lambda row: find_state(row['location']), axis=1)
    #df.to_csv("crystals_metadata_II.csv", sep=',')

def find_state(location):
    if pd.notnull(location):
        location = re.sub(r"(\w)([A-Z])", r"\1 \2", location) #(e.g. BrevigMission => Brevig Mission)
        #try:
        geolocator = Nominatim()
        loc = geolocator.geocode(location, language='en')
        country = loc.address.split(',')[-1].strip() # Get the country
        tmp_country = country.split(' ')
        tmp_country.append(country)
        tmp_country = set(tmp_country)
        ########################################################

        print tmp_country

        a = [transformations.cn_to_ctn(t) for t in tmp_country]

        for t in tmp_country:
            try:
            except:


        print a

            #print tmp_country
            #tmp_continent = [transformations.cn_to_ctn(word) for word in tmp_country]

            #print country, tmp_country, tmp_continent

            #for word in country:
            #    tmp_continent.append(transformations.cn_to_ctn(word)) # Get the continent
            #tmp_continent = filter(None, tmp_continent)
            #continent = '_'.join(tmp_continent)
            #return continent

        #except Exception as e:
        #    print e
        #    return "* Not found *"
    else:
        print "No location available"
        return ""


iterate(filename='./crystals_metadata.csv')
#iterate(filename='./test.csv')
