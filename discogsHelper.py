import discogs_client
from difflib import SequenceMatcher
def similar(name_returned, name):
    return SequenceMatcher(None, name_returned, name).ratio()

def discogs(name,d):
    try:
        results=d.search(name, type='artist')
        if (len(results)>0):
            first_result=d.search(name, type='artist')[0]
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
        except: genre='NaN'
    return  genre