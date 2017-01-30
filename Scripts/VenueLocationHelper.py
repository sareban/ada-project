# Preprocessing Helper for Switzerland Venues including google places
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
import math
from collections import Counter
import unicodedata
import VenueLocationHelper

warnings.filterwarnings('ignore')



def removeSpecialCharacters(input_string):
    input_string = str(input_string)
    while('-' in input_string or '+' in input_string or '=' in input_string or '.' in input_string or '\'' in input_string or '?' in input_string):
        input_string = input_string.replace('-','')
        input_string = input_string.replace('+','')
        input_string = input_string.replace('=','')
        input_string = input_string.replace('.','')
        input_string = input_string.replace('\'','')
        input_string = input_string.replace('?','')
    return input_string

def removeWords(input_string):
    input_string = str(input_string)
    while('(live)' in input_string ):
        input_string = input_string.replace('(live)','')
    return input_string

def removeSpaces(input_string):
    input_string = str(input_string)
    input_string = input_string.strip()
    return input_string

def replaceVenue_at(input_string):
    input_string = str(input_string)
    while '@' in input_string:
        position_venue_beginning = input_string.find('@')
        input_string = input_string[position_venue_beginning+1:]
        input_string = removeSpaces(input_string)
        input_string = replaceVenue_at(input_string)
    return input_string

def cleanVenueSpecificName(row, specific_name, specific_city, new_name):
    if specific_name in str(row['Venue']) and specific_city in str(row['City']):
            return new_name
    return row['Venue']


def correctVenueName(df, correct_name, incorrect_name):
    # This function corrects the venue with @incorrect_name to @correct_name in @df
    # If enough latitude, longitude, adress are present in the data to be modified, 
    #these data are assigned to the newly modified data, using argmax.
    
    df_tocorrect = df[df['Venue'].str.contains(incorrect_name,na=False,case = False) == True]
    df_coord = df_tocorrect[df_tocorrect['Latitude'].notnull()]
    df_adress = df_tocorrect[df_tocorrect['Adress'].notnull()]
    

    if len(df_coord)>math.floor(len(df_tocorrect)*2/3):

        #latitude = np.mean(df_coord['Latitude'])
        b = Counter(df_coord['Latitude'])
        latitude = b.most_common()[0][0]
        #longitude = np.mean(df_coord['Longitude'])
        b = Counter(df_coord['Longitude'])
        longitude = b.most_common()[0][0]

        df.loc[df['Venue'].str.contains(incorrect_name,na=False,case = False) == True, 'Latitude'] = latitude
        df.loc[df['Venue'].str.contains(incorrect_name,na=False,case = False) == True, 'Longitude'] = longitude
    else:
        df.loc[df['Venue'].str.contains(incorrect_name,na=False,case = False) == True, 'Latitude'] = np.nan
        df.loc[df['Venue'].str.contains(incorrect_name,na=False,case = False) == True, 'Longitude'] = np.nan
    if len(df_adress)>0:
        df.loc[df['Venue'].str.contains(incorrect_name,na=False,case = False) == True, 'Adress'] = df_adress.iloc[0]['Adress']
    
    df.loc[df['Venue'].str.contains(incorrect_name,na=False,case = False) == True, 'Venue'] = correct_name

    return df

def correctVenueNameCity(df, correct_name, incorrect_name, city):
    # This function corrects the venue with @incorrect_name to @correct_name in @df, using @city as aditional condition
    # If enough latitude, longitude, adress are present in the data to be modified, 
    #these data are assigned to the newly modified data, using argmax.

    df_tocorrect = df[(df['Venue'].str.contains(incorrect_name,na=False,case = False) == True) & 
                     (df['City'].str.contains(city,na=False,case = False) == True)]
    df_coord = df_tocorrect[df_tocorrect['Latitude'].notnull()]
    df_adress = df_tocorrect[df_tocorrect['Adress'].notnull()]

    if len(df_coord)>math.floor(len(df_tocorrect)*2/3):
        
        # We take the argmax
        #latitude = np.mean(df_coord['Latitude'])
        #longitude = np.mean(df_coord['Longitude'])
        b = Counter(df_coord['Latitude'])
        latitude = b.most_common()[0][0]
        b = Counter(df_coord['Longitude'])
        longitude = b.most_common()[0][0]

        df.loc[(df['Venue'].str.contains(incorrect_name,na=False,case = False)) & 
               (df['City'].str.contains(city,na=False,case = False)), 'Latitude'] = latitude
        df.loc[(df['Venue'].str.contains(incorrect_name,na=False,case = False)) & 
               (df['City'].str.contains(city,na=False,case = False)), 'Longitude'] = longitude
    else:
        df.loc[(df['Venue'].str.contains(incorrect_name,na=False,case = False)) & 
               (df['City'].str.contains(city,na=False,case = False)), 'Latitude'] = np.nan
        df.loc[(df['Venue'].str.contains(incorrect_name,na=False,case = False)) & 
               (df['City'].str.contains(city,na=False,case = False)), 'Longitude'] = np.nan    
    if len(df_adress)>0:
        df.loc[(df['Venue'].str.contains(incorrect_name,na=False,case = False)) & 
               (df['City'].str.contains(city,na=False,case = False)), 'Adress'] = df_adress.iloc[0]['Adress']

    
    df.loc[(df['Venue'].str.contains(incorrect_name,na=False,case = False)) & (df['City'].str.contains(city,na=False,case = False)), 'Venue'] = correct_name

    return df



def remove_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')



def cleanCity(total_events):
    total_events['City'] = total_events['City'].apply(lambda x: VenueLocationHelper.removeSpaces(x))
    total_events['City'] = total_events['City'].apply(lambda x: str(x).lower())
    total_events['City'] = total_events['City'].apply(lambda x: str(x).capitalize())

    total_events.loc[total_events['City'].str.contains('Genev',na=False,case = False) == True, 'City'] = 'Geneva'
    total_events.loc[total_events['City'].str.contains('Genèv',na=False,case = False) == True, 'City'] = 'Geneva'
    total_events.loc[total_events['City'].str.contains('genf',na=False,case = False) == True, 'City'] = 'Geneva'
    total_events.loc[total_events['City'].str.contains('Zurich',na=False,case = False) == True, 'City'] = 'Zürich'
    total_events.loc[total_events['City'].str.contains('Yverd',na=False,case = False) == True, 'City'] = 'Yverdon-les-bains'
    total_events.loc[total_events['City'].str.contains('base',na=False,case = False) == True, 'City'] = 'Basel'
    total_events.loc[total_events['City'].str.contains('bale',na=False,case = False) == True, 'City'] = 'Basel'
    return total_events





def cleanVenue(total_events):
    # Remove spaces 
    total_events['Venue'] = total_events['Venue'].apply(lambda x: VenueLocationHelper.removeSpaces(x))

    # Remove special characters in Venue name
    total_events['Venue'] = total_events['Venue'].apply(lambda x: VenueLocationHelper.removeSpecialCharacters(x))
    total_events['Venue'] = total_events['Venue'].apply(lambda x: VenueLocationHelper.replaceVenue_at(x))
    total_events['Venue'] = total_events['Venue'].apply(lambda x: VenueLocationHelper.remove_accents(x))


    # Put all the venue name in lower case:
    total_events['Venue'] = total_events['Venue'].apply(lambda x: str(x).lower())
    # Capitalize first letter only:
    total_events['Venue'] = total_events['Venue'].apply(lambda x: str(x).capitalize())

    total_events = VenueLocationHelper.correctVenueName(total_events, 'Paleo Festival','Paleo')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'D! Club','D!')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Palladium','palladium')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'La parenthese','paranthese')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'La parenthese','parenthese')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Zurich openair Festival','zurich openair')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Zurich openair Festival','zurich open air')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Caprice Festival','caprice')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Caribana Festival','caribana')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Balelec','ecole polytechnique')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Le Romandie','romandie')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Kofmehl','Kofmehl')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Meh suff Festival','Meh suf')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Montreux Jazz Festival','Montreux jazz')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Music summit Festival','Music summit')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'One FM','One fm')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Oxa','Oxa')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Rabadan','Rabadan')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'One FM','One fm')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Mad Club','mad','Lausanne')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Mad Club','mad','Genev')
    total_events = VenueLocationHelper.correctVenueName(total_events, 'Balelec','balalec')

    total_events.loc[(total_events['Venue'].str.contains('balelec',na=False,case = False)) & 
                   (total_events['City'].str.contains('lausanne',na=False,case = False) == False), 'Longitude'] = np.nan
    total_events.loc[(total_events['Venue'].str.contains('balelec',na=False,case = False)) & 
                   (total_events['City'].str.contains('lausanne',na=False,case = False) == False), 'Latitude'] = np.nan
    total_events.loc[(total_events['Venue'].str.contains('balelec',na=False,case = False)), 'City'] = 'Lausanne'
    
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Balelec','Balelec','Lausanne')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'L\' Usine a gaz','usine','nyon')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Bypass Club','bypass','Genev')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'gare d','gare d','Will')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Globull','globu','Bulle')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'GreenField festival','greenfield','Interlaken')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Gurten Festival','gurten','bern')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Hallenstadion','hallenstadion','zürich')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Hive club','hive','zürich')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Kaufleuten','Kaufleuten','zürich')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Maag Halle','Maag','zürich')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Planet 105','planet 105','zürich')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Street parade','streetparad','zürich')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'AMR','amr','Genev')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Kammgarn','Kammgarn','Schaffhausen')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Kasern','kasern','Basel')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Kiff','Kiff','aarau')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Kulturfabrik','Kulturfabrik','Solothurn')
    total_events.loc[(total_events['Venue'].str.contains('mica',na=False,case = False)) & 
                   (total_events['City'].str.contains('lausanne',na=False,case = False)), 'Longitude'] = np.nan
    total_events.loc[(total_events['Venue'].str.contains('mica',na=False,case = False)) & 
                   (total_events['City'].str.contains('lausanne',na=False,case = False)), 'Latitude'] = np.nan
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'mica Club','mica','lausanne')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Parterre','parter','Basel')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Picadilly','picad','Brugg')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Pont rouge','pont','Pont rouge')
    total_events = VenueLocationHelper.correctVenueNameCity(total_events, 'Kiff','Kiff','aarau')
    total_events.loc[(total_events['Venue'].str.contains('usine',na=False,case = False)) & 
                     (total_events['Venue'].str.contains('Kugler',na=False,case = False) == False) &
                     (total_events['Venue'].str.contains('Theatre',na=False,case = False) == False) & 
                     (total_events['City'].str.contains('genev',na=False,case = False)), 'Venue'] = 'L\' Usine'
    
    return total_events



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
    
    
    
    
    
def concatDataVenue():
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/
    
    filename = "total_venue_GooglePlace*.csv"
    folder = 'GooglePlaceData'
    fileAdress = os.path.join(folder, filename)
    all_files = glob.glob(fileAdress)
    df = pd.DataFrame()
    df = pd.concat((pd.read_csv(f) for f in all_files))

    #Reset the index
    df.reset_index(inplace = True,drop = True)


    # Save Again
    return df    
    
    