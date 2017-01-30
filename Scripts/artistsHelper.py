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
import bandsInTownHelper as bandsInTownHelper


def createArtistsDataFrame(filename):
    #Create a file containing all the artists, from a file containing events and artists
    
    df = pd.read_csv(filename)
    df = df[['Artist']]
    df = df.rename(columns={'Artist': 'name'})
    
    df2 = pd.DataFrame(columns=['genre', 'origin', 'no_result', 'ambigous_result'])
    df = pd.concat([df,df2])
                   
    # Keep only unique artists
    df.drop_duplicates(inplace=True)
    
    #Save to csv
    filename = '../Artists/total_artists.csv'
    pd.DataFrame(df, columns=list(df.columns)).to_csv(filename, index=False,encoding="utf-8")
    print('file saved')
    return df

def cleanArtistsDataFrame(filename):
    
    df = pd.read_csv(filename)
                   
    # Keep only unique artists
    df.drop_duplicates(inplace=True)

    
    #Save to csv
    pd.DataFrame(df, columns=list(df.columns)).to_csv(filename, index=False,encoding="utf-8",header = True)
    print('file saved')
    return df