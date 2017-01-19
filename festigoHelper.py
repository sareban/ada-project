# Festigo Parser for Switzerland
# Cyril Pecoraro

import requests
import pandas as pd
import urllib3
import json
import os


def requestFestigo():
    # this function makes a request to the Festigo API and save the JSON
    # input: /
    # output : /

    # Requesst
    baseUrl = 'https://www.festigo.ch/backend/api/festival/'
    data_json = requests.get(baseUrl).json()
    data_json = data_json['data']['data']
    print('Festigo request completed')

    # Save JSON
    folder = 'FestigoData'
    filename = 'festival_festigo.json'
    destinationFileName = os.path.join(folder, filename)
    with open(destinationFileName, 'w') as outfile:
        json.dump(data_json, outfile)
    print('Festigo JSON data saved to file')


def extractAdressField(df):
    # The JSON from Festigo is nested
    # Let's keep only tthe interesting fields (as specified above) and make them columns in the dataframe.
    # input: dataframe with adress cell to modify
    # output: modified dataframe

    i = 0
    for adress_json in df['address']:
        df.loc[i, 'postal_code'] = adress_json['postal_code']
        df.loc[i, 'city'] = adress_json['city']
        df.loc[i, 'canton'] = adress_json['canton']
        df.loc[i, 'coord_x'] = adress_json['coord_x']
        df.loc[i, 'coord_y'] = adress_json['coord_y']
        i += 1

    df.drop(['address'], axis=1, inplace=True)
    return df


def getDataFestigo():
    # The JSON from Festigo is nested
    # this function correctly extract all the desired information and fills a dataframe, and saves it to .csv file
    # input: JSON file
    # output : DataFrame

    # Request
    requestFestigo()

    # Read JSON file
    df = pd.read_json('.\festival_festigo.json')

    # Only keep useful columns
    col_to_keep = [
        "name",
        "description",
        "meta_desc",
        "website",
        "facebook_link",
        "ticket_link",
        "start_date",
        "end_date",
        "min_price",
        "max_price",
        "capacity",
        "is_free",
        "address"]

    df = df[col_to_keep]

    # Manage Adress Field which contains JSON
    df = extractAdressField(df)

    # Save the data to csv file
    filename = 'total_festigo.csv'
    pd.DataFrame(df, columns=list(df.columns)).to_csv(filename, index=False, encoding="utf-8")
    print('Festigo data saved to file')


    return df
