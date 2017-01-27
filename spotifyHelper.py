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
import csv
from multiprocessing import Process
import sys
import warnings
warnings.filterwarnings('ignore')


def spotifyRequest(base_url, name_request):
    # this function makes a request to the Spotify API
    # It takes between 0.25s and 0.76s for the request
    # input: parameters
    # output : JSON

    name_request = name_request.replace (" ", "+")
    name_request = name_request.replace("#","")
    request_url = base_url + '%22' + name_request + '%22&type=artist'
    data_json = requests.get(request_url).json()
    print(request_url)
    return data_json

def getDataSpotifyArtist(artist_name):
    # this function gets the genre and origin of artists using spotify API.
    # input: artistName
    # output : DataFrame row containing info about artist

    # Spotify request
    base_url = 'https://api.spotify.com/v1/search?q='
    data_json = spotifyRequest(base_url, artist_name)

    # Init
    artist_data_genre = np.nan
    artist_data_no_result = 0
    artist_data_ambigous_result = 0

    # DataFrame filling
    if 'artists' in data_json:
        result_artists_array = data_json['artists']['items']
        result_count = data_json['artists']['total']

        # No Artist found with this name
        if (result_count == 0):
            artist_data_no_result = 1

        # Several artists found with this name
        # We will take only the results where the name of the artists matchs exacty with the given data
        elif (result_count > 1):
            artist_data_ambigous_result = 1
            #Only select the exact matching name
            idx = []
            counter = 0
            for i,elem_json in enumerate(result_artists_array):
                if elem_json['name'].lower() == artist_name.lower():
                    # Exact matching, remember index in table of results given in the JSON
                    counter += 1
                    idx.append(i)
                    
            # Number of exact macthing needs to be exactly 1, otherwise it is ambigous
            if counter==1:
                matching_idx = idx[0]
                # Find genre 
                if ('genres' in result_artists_array[matching_idx]):
                    if (len(result_artists_array[matching_idx]['genres'])>0):
                        artist_data_genre = result_artists_array[matching_idx]['genres'][0]
                        artist_data_ambigous_result = 0

            elif counter>1:
                for matching_idx in idx:
                    # Find genre 
                    if ('genres' in result_artists_array[matching_idx]):
                        if (len(result_artists_array[matching_idx]['genres'])>0):
                            artist_data_genre = result_artists_array[matching_idx]['genres'][0]
                            artist_data_ambigous_result = 0
                            artist_data_no_result = 0

        # Unique Artist found with this name
        else:
            elem_json = result_artists_array[0]

            if ('genres' in elem_json):
                if (len(elem_json['genres'])>0):
                    artist_data_genre = elem_json['genres'][0]
                    
    else:
        raise Exception(1,'Servers overloading, waiting a bit...')
    return artist_data_genre, artist_data_no_result, artist_data_ambigous_result

def splitDataFrames(df):
    # This function split the dataframe in 4
    # input: dataFrame of artists
    # output : 4 DataFrame containing info about artists
    
    first_index = df.first_valid_index()
    last_index = df.last_valid_index()
    splitting = last_index/4
    df1 = df.ix[first_index:splitting]
    df2 = df.ix[splitting:splitting*2]
    df3 = df.ix[splitting*2:splitting*3]
    df4 = df.ix[splitting*3:last_index]
    return df1, df2, df3, df4


def getDataSpotifyGraph(df, df_index):
    # this function gets the genre and origin of all artists using MusicGraph API from a DataFrame and saves to .csv
    # input: dataFrame of artists
    # output : DataFrame containing info about artists
    
    start_time = time.time()
    loop_cter = 0
    dfout = pd.DataFrame()
   
    # Using 'Apply' is not faster here. Most of the time is spent in the request.
    for i, row in df.iterrows():
        print (i,'/',df.last_valid_index())
        dfrow = pd.DataFrame({'name': pd.Series(row['name']),
                                           'genre': pd.Series(row['genre']),
                                           'origin': pd.Series(row['origin']),
                                           'no_result': pd.Series(row['no_result']),
                                           'ambigous_result': pd.Series(row['ambigous_result']),
                                           })
        # If genre is missing, get information for this artist
        if (row['genre'] is np.nan or pd.isnull(row['genre'])):
            try:
                artist_data_genre, artist_no_result, artist_data_ambigous_result = getDataSpotifyArtist(row['name'])
            except Exception as inst:
                i, message = inst.args
                print(message)
                time.sleep(30)
                artist_data_genre, artist_no_result, artist_data_ambigous_result = getDataSpotifyArtist(row['name'])
                
            # Update the DataFrame with new information
            dfrow['genre'] = artist_data_genre
            dfrow['no_result'] = artist_no_result
            dfrow['ambigous_result'] = artist_data_ambigous_result
                                  
        # Concat
        dfout = pd.concat([dfout,dfrow])

        # Store
        saveDataSpotify(dfout,loop_cter, df_index)
        dfout = pd.DataFrame();
        loop_cter = 1
        
        if i%20==0:
            clear_output(wait=True)


    print("--- %s seconds ---" % (time.time() - start_time))
    #return df


def saveDataSpotify(df_artists, loop_cter, df_index):
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/

    folder = 'SpotifyData'
    filename = 'total_artists_Spotify'+str(df_index)+'.csv'
    destinationFileName = os.path.join(folder, filename)
    with open(destinationFileName, 'a') as f:
        if (loop_cter==0):
            pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(f, index=False, encoding="utf-8", header=True)
        else:
            pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(f, index=False, encoding="utf-8", header=False)

def concatDataSpotify():
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/
    
    filename = "total_artists_Spotify*.csv"
    folder = 'SpotifyData'
    fileAdress = os.path.join(folder, filename)
    all_files = glob.glob(fileAdress)
    df = pd.DataFrame()
    df = pd.concat((pd.read_csv(f) for f in all_files))

    #Reset the index
    df.reset_index(inplace = True,drop = True)


    # Save Again
    pd.DataFrame(df, columns=list(df.columns)).to_csv('total_artists_Spotify.csv', index=False, encoding="utf-8")
    return df

def concatSameData(indexFile):
    # this function concatenates the files df1, df11 etc and saves the dataframe to df1
    # input: dataFrame containing artists data
    # output :/


    folder = 'SpotifyData'

    filename = 'total_artists_Spotify'+str(indexFile)+'*.csv'
    fileAdress = os.path.join(folder, filename)
    all_files = glob.glob(fileAdress)
    df = pd.DataFrame()
    df = pd.concat((pd.read_csv(f) for f in all_files))

    #Reset the index
    df.reset_index(inplace = True,drop = True)

    # Save Again
    fileAdress_out = os.path.join(folder, 'total_artists_Spotify'+str(indexFile)+'.csv')
    pd.DataFrame(df, columns=list(df.columns)).to_csv(fileAdress_out, index=False, encoding="utf-8")
    return df

