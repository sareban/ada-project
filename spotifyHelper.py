# Spotify Parser for Switzerland Artists
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


def spotifyRequest(base_url, name_request):
    # this function makes a request to the Musicgraph API
    # input: parameters
    # output : JSON

    name_request = name_request.replace (" ", "+")
    name_request = name_request.replace("#","")
    request_url = base_url + '%22' + name_request + '%22&type=artist'
    data_json = requests.get(request_url).json()
    #print(request_url)
     
    return data_json


def  fillArtistDf(name, genre, no_result, ambigous_result):
    #Create a dataframe given parameters for the artist
    df_artist_data = pd.DataFrame({'name': pd.Series(name),
                                           'genre': pd.Series(genre),
                                           'no_result': pd.Series(no_result),
                                           'ambigous_result': pd.Series(ambigous_result),
                                           })
    return df_artist_data


def getDataSpotifyArtist(artist_name):
    # this function gets the genre and origin of artists using spotify API.
    # input: artistName
    # output : DataFrame row containing info about artist

    # MusicGraph request
    base_url = 'https://api.spotify.com/v1/search?q='
    name_request = artist_name
    data_json = spotifyRequest(base_url, name_request)

    # Init
    artist_musicgraph_genre = np.nan
    artist_musicgraph_origin = np.nan

    # DataFrame filling
    if 'artists' in data_json:
        result_artists_array = data_json['artists']['items']
        result_count = data_json['artists']['total']

        # No Artist found with this name
        if (result_count == 0):
            df_artist_data = fillArtistDf(artist_name, artist_musicgraph_genre, 1, 0)

        # Several Artist found with this name
        # We will take only the results where the name of the artists matchs exacty with the given data
        elif (result_count > 1):
            #Only select the exact matching name
            idx = 0
            counter = 0
            for i,elem_json in enumerate(result_artists_array):
                if elem_json['name'].lower() == artist_name.lower():
                    # Exact matching, remember index in table of results given in the JSON
                    counter += 1
                    idx = i
                    
            # Number of exact macthing needs to be exactly 1, otherwise it is ambigous
            if counter==1:
                # Find genre 
                if ('genres' in result_artists_array[idx]):
                    if (len(result_artists_array[idx]['genres'])>0):
                        artist_musicgraph_genre = result_artists_array[idx]['genres'][0]

                df_artist_data = fillArtistDf(artist_name, artist_musicgraph_genre, 0, 0)

            # Ambigous result
            else:
                df_artist_data = fillArtistDf(artist_name, artist_musicgraph_genre, 0, 1)

        # Unique Artist found with this name
        else:
            elem_json = result_artists_array[0]

            if ('genres' in elem_json):
                if (len(elem_json['genres'])>0):
                    artist_musicgraph_genre = elem_json['genres'][0]
                    
            df_artist_data = fillArtistDf(artist_name, artist_musicgraph_genre, 0, 0)

    else:
        raise Exception()
        
    return df_artist_data


def getDataSpotifyGraph(df):
    # this function gets the genre and origin of all artists using MusicGraph API from a DataFrame and saves to .csv
    # input: dataFrame of artists
    # output : DataFrame containing info about artists

    dfout = pd.DataFrame(columns=['genre', 'origin', 'no_result', 'ambigous_result'])
    loop_cter = 0
    
    for i, row in df.iterrows():
        df_artist_data = df.iloc[[i]]
        print(i, '/', len(df))
        
        # Get information for this artist
        if (row['genre'] is np.nan):
            try:
                df_artist_data = getDataSpotifyArtist(row['name'])
            except Exception as inst:
                time.sleep(30)
                print('Servers overloading, waiting a bit...')
                df_artist_data = getDataSpotifyArtist(row['name'])
                
            # Update the DataFrame with new information using the 'name' as the index
            df_artist_data['origin'] = row['origin']

        dfout = pd.concat([dfout,df_artist_data])   

        # Store
        if (i % 50 == 0 and i > 0):
            saveDataSpotify(dfout,loop_cter)
            dfout = pd.DataFrame();
            loop_cter = 1
        clear_output(wait=True)
        i+=1

    return df


def saveDataSpotify(df_artists, loop_cter):
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/

    folder = 'SpotifyData'
    filename = 'total_artists.csv'
    destinationFileName = os.path.join(folder, filename)
    with open(destinationFileName, 'a') as f:
        if (loop_cter==0):
            pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(f, index=False, encoding="utf-8", header=True)
        else:
            pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(f, index=False, encoding="utf-8", header=False)
    print('file saved')
