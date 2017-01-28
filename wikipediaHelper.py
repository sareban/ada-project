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


def wikipedia_get_info(df):
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



            try:
                origin=elements.find('th',text=re.compile('Origin')).findNext('td')
                origin=origin.contents[len(origin)-1]
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

            try:
                genre=elements.find('th',text=re.compile('Genres')).findNext('a').text
            except:
                genre='NaN'

                
            if( ',' in origin):
                origin=origin.rsplit(',', 1)[1]
            
            artist={}
            name_=rows['name']
            name=name_.lower()
            name=name.title()
            artist['name']=name
            artist['origin']=origin
            artist['genre']=genre
            list_of_artists=list_of_artists.append(artist, ignore_index=True)
        
        except:
            print('Not found on wikipedia')
            
    return list_of_artists
