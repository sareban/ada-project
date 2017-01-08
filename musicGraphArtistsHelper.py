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


def getDataMusicGraphArtist(artist_name):
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
            df_artist_data = pd.DataFrame({'name': pd.Series(artist_name),
                                           'genre': pd.Series(artist_musicgraph_genre),
                                           'origin': pd.Series(artist_musicgraph_origin),
                                           'no_result': pd.Series(1),
                                           'ambigous_result': pd.Series(0),
                                           })

        # Several Artist found with this name, will need further analysis
        elif (result_count > 1):
            df_artist_data = pd.DataFrame({'name': pd.Series(artist_name),
                                           'genre': pd.Series(artist_musicgraph_genre),
                                           'origin': pd.Series(artist_musicgraph_origin),
                                           'no_result': pd.Series(0),
                                           'ambigous_result': pd.Series(1),
                                           })

        # Unique Artist found with this name
        else:
            # Get MusicGraph metadata
            elem_json = data_json['data'][0]

            if ('main_genre' in elem_json):
                artist_musicgraph_genre = elem_json['main_genre']
            if ('country_of_origin' in elem_json):
                artist_musicgraph_origin = elem_json['country_of_origin']

            df_artist_data = pd.DataFrame({'name': pd.Series(artist_name),
                                           'genre': pd.Series(artist_musicgraph_genre),
                                           'origin': pd.Series(artist_musicgraph_origin),
                                           'no_result': pd.Series(0),
                                           'ambigous_result': pd.Series(0),
                                           })
    else:
        time.sleep(30)
        print('Waiting for the overlad')
        getDataMusicGraphArtist(artist_name)
    return df_artist_data


def getDataMusicGraph(df):
    # this function gets the genre and origin of all artists using MusicGraph API from a DataFrame and saves to .csv
    # input: dataFrame containing artists in column ['artist_name']
    # output : DataFrame containing info about artists

    # Initialize

    df_artists = pd.DataFrame(columns=['name', 'genre', 'origin', 'no_result', 'ambigous_result'])
    j = 1

    for i, row in df.iterrows():
        print(i, '/', len(df['artist_name']))
        df_artist_data = getDataMusicGraphArtist(row['artist_name'])
        df_artists = pd.concat([df_artists, df_artist_data])

        # Store
        if (i % 100 == 0 and i > 0):
            saveDataMusicGraph(df_artists, j)
            df_artists = pd.DataFrame(columns=['name', 'genre', 'origin', 'no_result', 'ambigous_result'])
            j += 1
        clear_output(wait=True)

    return df_artists


def saveDataMusicGraph(df_artists, j):
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/

    folder = 'MusicGraphArtistsData'
    filename = 'total_artists' + str(j) + '.csv'
    destinationFileName = os.path.join(folder, filename)
    pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(destinationFileName, index=False,
                                                                      encoding="utf-8")
    print('file', j, 'saved')
