# Google Places Helper for Switzerland Venues
# Cyril Pecoraro

import pandas as pd
import os
import glob
import urllib
import requests
import time
import numpy as np
import json
from pandas.io.json import json_normalize
from IPython.display import clear_output
from googleplaces import GooglePlaces, types, lang
import warnings
warnings.filterwarnings('ignore')

def getDataGooglePlace(df,api_key):
    loop_cter = 0
    api_key_index = 0
    dfout = pd.DataFrame()
    
    google_places = GooglePlaces(api_key)

    for i, row in df.iterrows():
        print (i,'/',df.last_valid_index())
        dfrow = pd.DataFrame({'Adress': pd.Series(row['Adress']),
                                        'City': pd.Series(row['City']),
                                        'Latitude': pd.Series(row['Latitude']),
                                        'Longitude': pd.Series(row['Longitude']),
                                        'Venue': pd.Series(row['Venue'])
                                           })
        dfrow['Latitude'] = round(dfrow['Latitude'],6)
        dfrow['Longitude'] = round(dfrow['Longitude'],6)
        
        if ((row['Longitude'] == np.nan or row['Longitude'] == np.nan) or (pd.isnull(row['Longitude']) or pd.isnull(row['Longitude']))):
            latitude = row['Longitude']
            logitude = row['Longitude']
            
            # If we have the adress let's use it. Oterwise, use city name
            if (pd.isnull(row['Adress']) == False):
                location_request = str(row['Adress'])+', '+str(row['City'])+', Switzerland'
            else: 
                location_request = str(row['City'])+', Switzerland'
                
            try:
                query_result = google_places.nearby_search(keyword=row['Venue'], location =location_request, radius =5000)

                print(row['Venue'])

                # If the exact place was found:
                if query_result.places:
                    place = query_result.places[0]
                    print(place.name)
                    latitude = round(float(place.geo_location['lat']),6)
                    longitude =round(float(place.geo_location['lng']),6)
                    if(latitude<45 or latitude>48 or longitude <5 or longitude>11):
                        raise Exception('Not found')
                else:
                    raise Exception('Not found')

            # Otherwise put coordinates of the city :
            except Exception as inst:
                message = inst.args
                print(message)
                query_result = google_places.text_search(query=location_request,radius=5000)
                if query_result.places:
                    place = query_result.places[0]
                    print(place.name)
                    latitude = round(float(place.geo_location['lat']),6)
                    longitude =round(float(place.geo_location['lng']),6)
                    if(latitude<45 or latitude>48 or longitude <5 or longitude>11):
                        latitude =np.nan
                        longitude = np.nan

            # Update row
            dfrow['Latitude'] = latitude
            dfrow['Longitude'] = longitude
        
         # Concat
        dfout = pd.concat([dfout,dfrow])

        # Store
        saveDataGooglePlace(dfout,loop_cter)
        dfout = pd.DataFrame();
        loop_cter = 1
        
        if i%20==0:
            clear_output(wait=True)


def saveDataGooglePlace(df,loop_cter):
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/

    folder = 'GooglePlaceData'
    filename = 'total_venue_GooglePlace.csv'
    destinationFileName = os.path.join(folder, filename)
    with open(destinationFileName, 'a') as f:
        if (loop_cter==0):
            pd.DataFrame(df, columns=list(df.columns)).to_csv(f, index=False, encoding="utf-8", header=True)
        else:
            pd.DataFrame(df, columns=list(df.columns)).to_csv(f, index=False, encoding="utf-8", header=False)
    
    
    
    
    
    