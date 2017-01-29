import pandas as pd
import numpy as np
import requests
import csv
import re
import bs4
import time
from bs4 import BeautifulSoup
import glob
import os
import wikipedia

csv_states=pd.read_csv('state_table.csv')
states=csv_states['name']
mylist=states.tolist()

def is_it_usa(origin):
    origin_=origin.title()
    if (origin_ in(mylist)):
        origin='United States'
    else:
        origin=origin
    return(origin)


def wikipedia_get_info(df,do_genre, do_origin,csv_name):
    url_base='https://en.wikipedia.org/wiki/'
    
    list_of_artists=pd.DataFrame(columns=['name','origin','genre'])
        
    for index, rows in df.iterrows():
        try:
            name_=rows['name']
            name = name_.replace(" ", "_")
            name=name.lower()
            name=name.title()
            url=url_base+name
            r=requests.get(url)
            soup=BeautifulSoup(r.content,'html.parser')
            elements=soup.find('table')

            if(do_origin==1 and pd.isnull(rows['origin']) ):

                try:
                    origin=elements.find('th',text=re.compile('Origin')).findNext('td')
                    origin=origin.contents[len(origin)-1]
                    if(isinstance(origin, str)==0):
                        origin=origin.text
                except: 
                    origin='NaN'
                    
            
                if(origin=='NaN'):
                    try:
                        origin=elements.find('th',text=re.compile('Born')).findNext('span', {'class':'birthplace'}).text
                    except:
                        origin=origin
                
                if(origin=='NaN'):
                    try:
                        origin=elements.find('th',text=re.compile('Born')).findNext('span', {'class':'nowrap'})
                
                        origin=origin.contents[len(origin)-1].text            
                    except:
                        origin=origin
                
                if (origin=='NaN') or (isinstance(origin, str)==0):
                    try:
                        origin=elements.find('th',text=re.compile('Born')).findNext('td')                
                        origin=origin.contents[len(origin)-1]
                        if(isinstance(origin, str)==0):
                            origin=origin.text
                
                    except:
                        origin=origin
            else:
                origin=rows['origin']
            if(do_genre==1 and pd.isnull(rows['genre'])):
                try:
                    genre=elements.find('th',text=re.compile('Genres')).findNext('a').text
                except:
                    genre='NaN'
            else:
                genre=rows['genre']

            if(isinstance(origin, str)==0 and origin.isnotnull):
                origin=origin.text
            if( '>' in origin):
                origin=origin.rsplit('<', 1)[0]
                origin=origin.rsplit('>', 1)[1]

            if( ',' in origin):
                origin=origin.rsplit(',', 1)[1]
            
            artist={}
            name=rows['name']                
            artist['name']=name
            origin=is_it_usa(origin)
            artist['origin']=origin
            artist['genre']=genre
            list_of_artists=list_of_artists.append(artist, ignore_index=True)
        
        except:
            print('Not found on wikipedia')

    list_of_artists.to_csv(csv_name, index=False, encoding='utf-8')


    return list_of_artists

def splitDataFrames(df):
    # This function split the dataframe in 4
    # input: dataFrame of artists
    # output : 4 DataFrame containing info about artists
    
    first_index = df.first_valid_index()
    last_index = df.last_valid_index()
    splitting = last_index/2
    df1 = df.ix[first_index:splitting]
    df2 = df.ix[splitting:last_index]
    
    return df1, df2


