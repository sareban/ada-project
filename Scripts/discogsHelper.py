import discogs_client
from difflib import SequenceMatcher
import time

def similar(name_returned, name):
    return SequenceMatcher(None, name_returned, name).ratio()

def discogs(df,csv_name,d):
    for index, rows in df.iterrows():
        time.sleep(5)
        name=rows['name']
        try:
            results=d.search(name, type='artist')
            if (len(results)>0):
                time.sleep(1)
                first_result=d.search(name, type='artist')[0]
                time.sleep(1)
                name_returned=first_result.name
                similarity=similar(name_returned, name)
                if (similarity>0.75):
                    all_releases=first_result.releases
                    if (len(all_releases)>0):
                        first_release=all_releases[0]
                        genre=first_release.genres[0]
                    else:
                        genre='Nan'
                else:
                    genre='NaN'
            else:
                genre='NaN'
               
        except: 
            genre='NaN'
            print('Server Overloading')
            traceback.print_tb


                
        df.set_value(index,'genre',genre)
    list_of_artists.to_csv(csv_name, index=False, encoding='utf-8')

    return  genre