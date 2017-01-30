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
import unicodedata

warnings.filterwarnings('ignore')

def remove_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def getDataGooglePlace(df,api_key, df_idx):
    not_found_cter = 0
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
        latitude = round(dfrow['Latitude'],6)
        longitude = round(dfrow['Longitude'],6)
        dfrow['Latitude'] = latitude
        dfrow['Longitude'] =longitude
        
        if ((row['Latitude'] == np.nan or row['Longitude'] == np.nan) or (pd.isnull(row['Latitude']) or pd.isnull(row['Longitude']))):
            flag = 0
            retry = 0

            
            # If we have the adress and the city:
            if ((pd.notnull(row['Adress']) or  ( row['Adress'] is np.nan == False)) and 
                (pd.notnull(row['City']) or  (row['City'] is np.nan == False) or row['City'] != 'Nan'  )):
                location_request = str(row['Adress'])+', '+str(row['City'])+', Switzerland'
                
            # If we have the adress but not the city:
            elif ((pd.notnull(row['Adress']) or  ( row['Adress'] is np.nan == False)) and 
                ((pd.isnull(row['City']) or  (row['City'] is np.nan == True)) and row['City'] == 'Nan'  )):
                location_request = str(row['Adress'])+', ' + 'Switzerland'   
                
            # If we have only the city 
            elif ((pd.notnull(row['City']) or  (row['City'] is np.nan == False)) and (row['City'] != 'Nan'  )): 
                location_request = str(row['City'])+', Switzerland'
                
            #else just specify the country
            else:
                location_request = 'Switzerland'
                flag = 1
     
            try:
                print('To find :',row['Venue'],' in ', location_request)
                
                #As there is only the country specified, this research must be done in-depth
                if flag == 1:
                    query_result = google_places.text_search(query=row['Venue'], location = location_request, radius = 5000)
                else:
                    query_result = google_places.nearby_search(keyword=row['Venue'], location = location_request, radius = 5000)

                # If the exact place was found:
                if query_result.places:
                    place = query_result.places[0]
                    print('Found :', place.name)
                    latitude = round(float(place.geo_location['lat']),6)
                    longitude =round(float(place.geo_location['lng']),6)
                    if(latitude<45 or latitude>48 or longitude <5 or longitude>11):
                        raise Exception('Not found')
                else:
                    raise Exception('Not found')

            # Try a more in-depth research
            except Exception as inst:
                message = inst.args
                print(message)
                query_result = google_places.text_search(query=row['Venue'], location = location_request, radius = 5000)

                if query_result.places:
                    place = query_result.places[0]
                    print('Finally, Found :', place.name)
                    latitude = round(float(place.geo_location['lat']),6)
                    longitude =round(float(place.geo_location['lng']),6)
                    if(latitude<45 or latitude>48 or longitude <5 or longitude>11):
                        retry = 1
                else: 
                    retry = 1
                
                # Try to search just for the location of the place, whithout its name
                if retry == 1:
                    query_result = google_places.text_search(query=location_request, radius = 5000)
                    if query_result.places:
                        place = query_result.places[0]
                        print('Could only find the location :', place.name)
                        latitude = round(float(place.geo_location['lat']),6)
                        longitude =round(float(place.geo_location['lng']),6)
                    
                        # Nothing was found
                        if(latitude<45 or latitude>48 or longitude <5 or longitude>11 or flag == 1):
                            latitude = np.nan
                            longitude = np.nan
                            not_found_cter += 1
                            print('NAN - Finally Not found')

    

            # Update row
            dfrow['Latitude'] = latitude
            dfrow['Longitude'] = longitude
        
         # Concat
        dfout = pd.concat([dfout,dfrow])

        # Store
        saveDataGooglePlace(dfout,loop_cter,df_idx)
        dfout = pd.DataFrame();
        loop_cter = 1
        
        if i%50==0:
            clear_output(wait=True)
            print('Not exactly found up to here: ', not_found_cter)
    return not_found_cter


def saveDataGooglePlace(df,loop_cter,df_idx):
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/

    folder = 'GooglePlaceData'
    filename = 'total_venue_GooglePlace'+str(df_idx)+'.csv'
    destinationFileName = os.path.join(folder, filename)
    with open(destinationFileName, 'a') as f:
        if (loop_cter==0):
            pd.DataFrame(df, columns=list(df.columns)).to_csv(f, index=False, encoding="utf-8", header=True)
        else:
            pd.DataFrame(df, columns=list(df.columns)).to_csv(f, index=False, encoding="utf-8", header=False)
    
    
    
    
    
    