# MusicGraph Parser for Switzerland Artists
# Cyril Pecoraro

import pandas as pd
import os
import glob
import urllib
import requests
import time
import json
from pandas.io.json import json_normalize
from IPython.display import clear_output
import numpy as np
import sys
import warnings
warnings.filterwarnings('ignore')

def musicGraphRequest(base_url, param_request):
    # this function makes a request to the Musicgraph API
    # input: parameters
    # output : JSON

    request_url = base_url + '&' + urllib.parse.urlencode(param_request, doseq=True)
    # Wait to respect API limits
    time.sleep(2)
    data_json = requests.get(request_url).json()
    #print(request_url)

    return data_json

def fillArtistDf(name, genre, origin, no_result, ambigous_result):
    #Create a dataframe given parameters for the artist
    df_artist_data = pd.DataFrame({'name': pd.Series(name),
                                           'genre': pd.Series(genre),
                                           'origin': pd.Series(origin),
                                           'no_result': pd.Series(no_result),
                                           'ambigous_result': pd.Series(ambigous_result),
                                           })
    return df_artist_data
    
def getDataMusicGraphArtist(row, type_request, api_key):
    
    # this function gets the genre and origin of artists using MusicGraph API.
    # input: artistName
    # output : DataFrame row containing info about artist

    # MusicGraph request
    artist_name = row['name']
    base_url_id = 'http://api.musicgraph.com/api/v2/artist/search?api_key=377a8c2a14bbb912a0e5907822613e14&limit=10'
    param_request = {'name': artist_name, 'api_key': api_key}
    data_json = musicGraphRequest(base_url_id, param_request)

    # Init
    dfrow = fillArtistDf(row['name'],row['genre'],row['origin'],row['no_result'],row['ambigous_result'])
    if 'status' in data_json:
        if 'code' in data_json['status']:
            if data_json['status']['code'] == 3:
                raise Exception(3,'Maximum number of API calls exceded')
            
    # DataFrame filling
    if 'pagination' in data_json:
        result_count = data_json['pagination']['count']

        # No Artist found with this name
        if (result_count == 0):
            #df_artist_data = fillArtistDf(artist_name, artist_musicgraph_genre, artist_musicgraph_origin, 1, 0)
            dfrow['no_result'] = 1
            dfrow['ambigous_result'] = 0

        # Several Artist found with this name, will need further analysis
        elif (result_count > 1):
            dfrow['ambigous_result'] = 1
            dfrow['no_result'] = 0

        # Unique Artist found with this name
        else:
            # Get MusicGraph metadata
            elem_json = data_json['data'][0]

            # Checking that tags exist
            if ('main_genre' in elem_json):
                artist_musicgraph_genre = elem_json['main_genre']
            else: artist_musicgraph_genre = np.nan
            if ('country_of_origin' in elem_json):
                artist_musicgraph_origin = elem_json['country_of_origin']
            else: artist_musicgraph_origin = np.nan
            
            # If the missing information was the genre:
            if type_request == 'g':
                dfrow['genre'] = artist_musicgraph_genre
                dfrow['no_result'] = 0
                dfrow['ambigous_result'] = 0
                                           
            # If the missing information was the origin:    
            elif type_request == 'o':
                dfrow['origin'] = artist_musicgraph_origin
                dfrow['no_result'] = 0
                dfrow['ambigous_result'] = 0
                                           
            # If the missing information was the origin AND the genre:    
            elif type_request == 'a':
                dfrow['origin'] = artist_musicgraph_origin
                dfrow['genre'] = artist_musicgraph_genre
                dfrow['no_result'] = 0
                dfrow['ambigous_result'] = 0
    else:
        raise Exception(1,'Servers overloading, waiting a bit...')
    
    return dfrow


def getDataMusicGraph(df, api_key):
    # this function gets the genre and origin of all artists using MusicGraph API from a DataFrame and saves to .csv
    # input: dataFrame of artists
    # output : DataFrame containing info about artists

    loop_cter = 0
    dfout = pd.DataFrame()


    # Using 'Apply' is not faster here. Most of the time is spent in the request.
    for i, row in df.iterrows():
        print (i,'/',df.last_valid_index())
        dfrow = fillArtistDf(row['name'],row['genre'],row['origin'],row['no_result'],row['ambigous_result'])
                
        # If genre is missing, get information for this artist
        if (row['genre'] is np.nan or row['origin'] is np.nan or 
           pd.isnull(row['genre']) or  pd.isnull(row['origin'])):
            if (row['genre'] is np.nan or pd.isnull(row['genre'])):
                type_request = 'g'
            elif (row['origin'] is np.nan or  pd.isnull(row['origin'])):
                type_request = 'o'
            elif ((row['genre'] is np.nan and row['origin'] is np.nan) or 
                  pd.isnull(row['genre']) and  pd.isnull(row['origin'])):
                type_request = 'a'
                
            try:
                # Get information for this artist
                dfrow = getDataMusicGraphArtist(row, type_request, api_key)
                

            except Exception as inst:
                i, message = inst.args
                print(message)
                if i==1:
                    time.sleep(30)
                    dfrow = getDataMusicGraphArtist(row,type_request)
                else: sys.exit(message)
                
        # Concat
        dfout = pd.concat([dfout,dfrow])

        # Store
        if (i % 10 == 0 and i > 0):
            saveDataMusicGraph(df,loop_cter)
            loop_cter = 1
        clear_output(wait=True)

    return df


def saveDataMusicGraph(df_artists,loop_cter):
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/

    folder = 'MusicGraphArtistsData'
    filename = 'total_artists_MusicGraph.csv'
    destinationFileName = os.path.join(folder, filename)
    with open(destinationFileName, 'a') as f:
        if (loop_cter==0):
            pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(f, index=False, encoding="utf-8", header=True)
        else:
            pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(f, index=False, encoding="utf-8", header=False)
    print('file saved')
    clear_output(wait=True)
