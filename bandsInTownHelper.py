# BandsInTown Parser for Switzerland
# Cyril Pecoraro

import requests
import glob
import pandas as pd
import time
import json
import os
from pandas.io.json import json_normalize
from IPython.display import clear_output


def getDateRequestParam(day, month, year):
    # this function formats the date in the correct form for the request to the BandsInTown API
    # input: parameters
    # output : Date

    date = str(year) + '-' + str("%02d" % month) + '-' + str("%02d" % day)
    date_request = date + '-' + date
    return date_request


def bandsInTownRequest(base_url, date_request, city_request):
    # this function makes a request to the BandsInTown API
    # input: parameters
    # output : JSON

    request_url = base_url + '&location=' + city_request + '&date=' + date_request
    data_json = requests.get(request_url).json()
    return data_json


def fillPandasJson(data_json):
    # The JSON from BandsIntown is nested
    # this function correctly extract all the desired information and fills a dataframe
    # input: JSON
    # output : DataFrame

    df_city = pd.DataFrame()
    if len(data_json) > 0:

        # If Overload of servor, raise an error
        if 'errors' in data_json:
            raise Exception()

        if 'artists' in data_json[0]:
            df_city = pd.io.json.json_normalize(data_json, meta_prefix='event_',
                                                meta=['id', 'datetime', 'url',
                                                      ['venue', 'name'],
                                                      ['venue', 'url'],
                                                      ['venue', 'id'],
                                                      ['venue', 'city'],
                                                      ['venue', 'region'],
                                                      ['venue', 'country'],
                                                      ['venue', 'latitude'],
                                                      ['venue', 'longitude']]
                                                , record_path='artists', record_prefix='artist_')
        if len(df_city) > 0:
            df_city = df_city[df_city['event_venue.country'] == 'Switzerland']
    return df_city


def getDataBandsInTown(starting_year, ending_year):
    # this function gets all the data from BandsInTown in Switzerland between 2 years.
    # It will save the data every month to a different .csv file
    # input: starting and ending years
    # output : None

    base_url = 'http://api.bandsintown.com/events/search.json?api_version=2.0&app_id=epfl&radius=50'
    cities = [
        'Geneva,Switzerland',
        'Lausanne,Switzerland',
        'Lucerne,Switzerland',
        'Zurich,Switzerland',
        'Bern,Switzerland',
        'Basel,Switzerland',
        'Locarno,Switzerland',
    ]

    for year in range(starting_year, ending_year + 1):
        for month in range(1, 13):
            df = pd.DataFrame()
            for day in range(1, 32):
                for city_request in cities:

                    print('Now processing:', day, '/', month, '/', year, city_request)

                    date_request = getDateRequestParam(day, month, year)
                    data_json = bandsInTownRequest(base_url, date_request, city_request)

                    try:
                        df_city = fillPandasJson(data_json)

                    # Error in the response of the server, due to overloading, wait and try again
                    except Exception as inst:
                        print('Servers overloading, waiting a bit...')
                        time.sleep(20)
                        data_json = bandsInTownRequest(base_url, date_request, city_request)
                        df_city = fillPandasJson(data_json)

                    # Concatenate the data from this city with the other city for the same month
                    df = pd.concat([df, df_city])

                    # Avoid duplicates in the dataframe of this month 
                    # (can happen as some events appear in the response of several cities)
                    if len(df) > 0:
                        df.drop_duplicates(inplace=True)

                clear_output(wait=True)

            # Save the data for the current month to csv file in a subdirectory
            # Drop useless columns
            if set(['artist_mbid', 'event_venue.country']).issubset(df.columns):
                df.drop(['artist_mbid', 'event_venue.country'], axis=1, inplace=True)

            folder = 'BandsInTownData'
            filename = 'bands_in_town' + str("%02d" % month) + '-' + str(year) + '.csv'
            destinationFileName = os.path.join(folder, filename)

            pd.DataFrame(df, columns=list(df.columns)).to_csv(destinationFileName, index=False, encoding="utf-8")
            print(month, '/', year, ' saved to file')


def concatenateDataBandsInTown():
    # this function concatenate the csv file create by the function getDataBandsInTown into 1 big csv file
    # It also deletes duplicates that might happen between end of months/beginning of months
    # input: /
    # output : DataFrame with all the Data

    filename = "bands_in_town*.csv"
    folder = 'BandsInTownData'
    fileAdress = os.path.join(folder, filename)
    all_files = glob.glob(fileAdress)
    df = pd.DataFrame()
    df = pd.concat((pd.read_csv(f) for f in all_files))

    # Drop possible duplicates
    df.drop_duplicates(inplace=True)

    # Save Again
    return df
