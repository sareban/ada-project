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
    base_url_id = 'http://api.musicgraph.com/api/v2/artist/search?limit=10'
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
            dfrow['no_result'] = 1
            dfrow['ambigous_result'] = 0

        # Several Artist found with this name, will need further analysis
        elif (result_count > 1):
            artist_musicgraph_genre = np.nan
            artist_musicgraph_origin = np.nan
            result_artists_array=data_json['data']
            artist_data_ambigous_result = 1
            artist_data_no_result = 1
            
            #Only select the exact matching name
            idx = []
            counter = 0
            for i,elem_json in enumerate(result_artists_array):
                if elem_json['name'].lower() == artist_name.lower():
                    # Exact matching, remember index in table of results given in the JSON
                    counter += 1
                    idx.append(i)
                    
            # Number of exact macthing needs to be exactly 1
            # If there are more than 1 artist with the exact right name, take the one which has a genre and origin specified
            if counter==1:
                matching_idx = idx[0]
                artist_data_ambigous_result = 0
                artist_data_no_result = 0
                # Find genre 
                if ('main_genre' in result_artists_array[matching_idx]):
                    artist_musicgraph_genre = result_artists_array[matching_idx]['main_genre']
                if ('country_of_origin' in result_artists_array[matching_idx]):
                    artist_musicgraph_origin = result_artists_array[matching_idx]['country_of_origin']
                        
            elif counter>1:
                for matching_idx in idx:
                    # Find genre 
                    if ('main_genre' in result_artists_array[matching_idx]):
                        artist_musicgraph_genre = result_artists_array[matching_idx]['main_genre']
                        artist_data_ambigous_result = 0
                        artist_data_no_result = 0
                    if ('country_of_origin' in result_artists_array[matching_idx]):
                        artist_musicgraph_origin = result_artists_array[matching_idx]['country_of_origin']
                        artist_data_ambigous_result = 0
                        artist_data_no_result = 0
                
                    # If the missing information was the genre:
            if type_request == 'g':
                dfrow['genre'] = artist_musicgraph_genre
                dfrow['no_result'] = artist_data_no_result
                dfrow['ambigous_result'] = artist_data_ambigous_result
                                           
            # If the missing information was the origin:    
            elif type_request == 'o':
                dfrow['origin'] = artist_musicgraph_origin
                dfrow['no_result'] = artist_data_no_result
                dfrow['ambigous_result'] = artist_data_ambigous_result
                                           
            # If the missing information was the origin AND the genre:    
            elif type_request == 'a':
                dfrow['origin'] = artist_musicgraph_origin
                dfrow['genre'] = artist_musicgraph_genre
                dfrow['no_result'] = artist_data_no_result
                dfrow['ambigous_result'] = artist_data_ambigous_result
                

        # Unique Artist found with this name
        else:
            # Get MusicGraph metadata
            elem_json = data_json['data'][0]
            artist_data_no_result = 1

            # Checking that tags exist
            if ('main_genre' in elem_json):
                artist_musicgraph_genre = elem_json['main_genre']
                artist_data_no_result = 0
            else: artist_musicgraph_genre = np.nan
            if ('country_of_origin' in elem_json):
                artist_musicgraph_origin = elem_json['country_of_origin']
                artist_data_no_result = 0
            else: artist_musicgraph_origin = np.nan
            
            # If the missing information was the genre:
            if type_request == 'g':
                dfrow['genre'] = artist_musicgraph_genre
                dfrow['no_result'] = artist_data_no_result
                dfrow['ambigous_result'] = 0
                                           
            # If the missing information was the origin:    
            elif type_request == 'o':
                dfrow['origin'] = artist_musicgraph_origin
                dfrow['no_result'] = artist_data_no_result
                dfrow['ambigous_result'] = 0
                                           
            # If the missing information was the origin AND the genre:    
            elif type_request == 'a':
                dfrow['origin'] = artist_musicgraph_origin
                dfrow['genre'] = artist_musicgraph_genre
                dfrow['no_result'] = artist_data_no_result
                dfrow['ambigous_result'] = 0
    else:
        raise Exception(1,'API Key expired or servers overloading')
        
    return dfrow


def getDataMusicGraph(df, df_index, api_key):
    # this function gets the genre and origin of all artists using MusicGraph API from a DataFrame and saves to .csv
    # input: dataFrame of artists
    # output : DataFrame containing info about artists

    loop_cter = 0
    api_key_index = 0
    dfout = pd.DataFrame()


    # Using 'Apply' is not faster here. Most of the time is spent in the request.
    for i, row in df.iterrows():
        print (i,'/',df.last_valid_index())
        dfrow = fillArtistDf(row['name'],row['genre'],row['origin'],row['no_result'],row['ambigous_result'])
                
        # If genre is missing, get information for this artist
        if ((row['genre'] is np.nan and row['origin'] is np.nan) or (pd.isnull(row['genre']) and pd.isnull(row['origin']))):
            type_request = 'a'
        elif (row['genre'] is np.nan or pd.isnull(row['genre'])):
            type_request = 'g'
        elif (row['origin'] is np.nan or pd.isnull(row['origin'])):
            type_request = 'o'
                
        try:
                # Get information for this artist
            dfrow = getDataMusicGraphArtist(row, type_request, api_key[api_key_index])                

        except Exception as inst:
            i, message = inst.args
            print(message)
            print('Key expired : changing key')
            
            if (api_key_index<len(api_key)-1):
                api_key_index+=1
            else: 
                api_key_index = 0
            dfrow = getDataMusicGraphArtist(row,type_request, api_key[api_key_index])
                
                
        # Concat
        dfout = pd.concat([dfout,dfrow])

        # Store
        saveDataMusicGraph(dfout,loop_cter,df_index)
        dfout = pd.DataFrame()
        loop_cter = 1
        if i%20==0:
            clear_output(wait=True)

    return dfout


def saveDataMusicGraph(df_artists,loop_cter, df_index):
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/

    folder = 'MusicGraphArtistsData'
    filename = 'total_artists_MusicGraph'+str(df_index)+'.csv'
    destinationFileName = os.path.join(folder, filename)
    with open(destinationFileName, 'a') as f:
        if (loop_cter==0):
            pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(f, index=False, encoding="utf-8", header=True)
        else:
            pd.DataFrame(df_artists, columns=list(df_artists.columns)).to_csv(f, index=False, encoding="utf-8", header=False)
    
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

def concatDataMusicGraph():
    # this function saves the dataframe to csv
    # input: dataFrame containing artists data
    # output :/
    
    filename = "total_artists_MusicGraph*.csv"
    folder = 'MusicGraphArtistsData'
    fileAdress = os.path.join(folder, filename)
    all_files = glob.glob(fileAdress)
    df = pd.DataFrame()
    df = pd.concat((pd.read_csv(f) for f in all_files))

    #Reset the index
    df.reset_index(inplace = True,drop = True)


    # Save Again
    pd.DataFrame(df, columns=list(df.columns)).to_csv('total_artists_MusicGraph.csv', index=False, encoding="utf-8")
    print('file saved')
    return df

