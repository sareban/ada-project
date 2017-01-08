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


def musicGraphRequest(base_url, param_request):
    # this function makes a request to the Musicgraph API
    # input: parameters
    # output : JSON

    request_url = base_url + '&' + urllib.parse.urlencode(param_request, doseq=True)
    # Wait to respect API limits
    time.sleep(0.5)
    data_json = requests.get(request_url).json()

    return data_json

def  fillArtistDf(name, genre, origin, no_result, ambigous_result):
    #Create a dataframe given parameters for the artist
    df_artist_data = pd.DataFrame({'name': pd.Series(name),
                                           'genre': pd.Series(genre),
                                           'origin': pd.Series(origin),
                                           'no_result': pd.Series(no_result),
                                           'ambigous_result': pd.Series(ambigous_result),
                                           })
    return df_artist_data
    
def getDataMusicGraphArtist(artist_name, type):
    
    # this function gets the genre and origin of artists using MusicGraph API.
    # input: artistName
    # output : DataFrame row containing info about artist

    # MusicGraph request
    base_url_id = 'http://api.musicgraph.com/api/v2/artist/search?api_key=377a8c2a14bbb912a0e5907822613e14&limit=10'
    param_request = {'name': artist_name, 'api_key': '377a8c2a14bbb912a0e5907822613e14'}
    data_json = musicGraphRequest(base_url_id, param_request)

    # Init
    artist_musicgraph_genre = np.nan
    artist_musicgraph_origin = np.nan

    # DataFrame filling
    if 'pagination' in data_json:
        result_count = data_json['pagination']['count']

        # No Artist found with this name
        if (result_count == 0):
            #df_artist_data = fillArtistDf(artist_name, artist_musicgraph_genre, artist_musicgraph_origin, 1, 0)
            df_artist_data = pd.DataFrame({'name': pd.Series(artist_name),'no_result': pd.Series(1),'ambigous_result': pd.Series(0)})

        # Several Artist found with this name, will need further analysis
        elif (result_count > 1):
            df_artist_data = pd.DataFrame({'name': pd.Series(artist_name),'ambigous_result': pd.Series(1),'no_result': pd.Series(0)})


        # Unique Artist found with this name
        else:
            # Get MusicGraph metadata
            elem_json = data_json['data'][0]

            # Checking that tags exist
            if ('main_genre' in elem_json):
                artist_musicgraph_genre = elem_json['main_genre']
            if ('country_of_origin' in elem_json):
                artist_musicgraph_origin = elem_json['country_of_origin']
            
            # If the missing information was the genre:
            if type == 'g':
                df_artist_data = pd.DataFrame({
                                            'name': pd.Series(artist_name),
                                           'genre': pd.Series(artist_musicgraph_genre),
                                           'no_result': pd.Series(0),
                                           'ambigous_result': pd.Series(0),
                                           })
                                           
            # If the missing information was the origin:    
            elif type == 'o':
                df_artist_data = pd.DataFrame({
                                           'name': pd.Series(artist_name),
                                           'origin': pd.Series(artist_musicgraph_origin),
                                           'no_result': pd.Series(0),
                                           'ambigous_result': pd.Series(0),
                                           }) 
                                           
            # If the missing information was the origin AND the genre:    
            elif type == 'a':
                df_artist_data = pd.DataFrame({
                                           'name': pd.Series(artist_name),
                                           'genre': pd.Series(artist_musicgraph_genre),
                                           'origin': pd.Series(artist_musicgraph_origin),
                                           'no_result': pd.Series(0),
                                           'ambigous_result': pd.Series(0),
                                           })                                                                                   

    else:
        raise Exception()
    
    return df_artist_data


def getDataMusicGraph(df):
    # this function gets the genre and origin of all artists using MusicGraph API from a DataFrame and saves to .csv
    # input: dataFrame of artists
    # output : DataFrame containing info about artists


    for i, row in df.iterrows():
        print(i, '/', len(df))
        try:
            if (row['genre'] is np.nan or row['origin'] is np.nan):
                if (row['genre'] is np.nan):
                    type = 'g'
                elif (row['origin'] is np.nan):
                    type = 'o'
                elif (row['genre'] is np.nan and row['origin'] is np.nan):
                    type = 'a'
                
                # Get information for this artist
                df_artist_data = getDataMusicGraphArtist(row['name'], type)
                # Update the DataFrame with new information using the 'name' as the index
                df.set_index('name', inplace=True)
                df_artist_data.set_index('name', inplace=True)
                df.update(df_artist_data)
                df.reset_index(inplace=True)
             
        except Exception as inst:
            time.sleep(30)
            print('Servers overloading, waiting a bit...')
            df_artist_data = getDataMusicGraphArtist(row['name'],type)
        
      

        # Store
        if (i % 100 == 0 and i > 0):
            saveDataMusicGraph(df)
        clear_output(wait=True)

    return df


def saveDataMusicGraph(df_artists):
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/

    folder = 'MusicGraphArtistsData'
    filename = 'total_artists.csv'
    destinationFileName = os.path.join(folder, filename)
    pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(destinationFileName, index=False,
                                                                      encoding="utf-8")
    print('file saved')
