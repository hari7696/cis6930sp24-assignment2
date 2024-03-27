from geopy.geocoders import GoogleV3
import pandas as pd
from utilities import determine_side_of_town, unpickle_object, pickle_object, get_coordinates
import os
def extract_feilds(df):

    #day of week extraction
    df['Day of the Week'] = pd.to_datetime(df['incident_time'], format = '%d/%m/%Y %H:%M' ).dt.day_name()

    dict_week_day_to_num = {
        'Sunday': 1,
        'Monday': 2,
        'Tuesday': 3,
        'Wednesday': 4,
        'Thursday': 5,
        'Friday': 6,
        'Saturday': 7
    }

    df['Day of the Week'] = df['Day of the Week'].apply(lambda x: dict_week_day_to_num[x])

    #time of the day extraction
    df['Time of the Day'] = pd.to_datetime(df['incident_time'], format = '%d/%m/%Y %H:%M' ).dt.hour

    #weather
    

    #Location Rank

    dict_location_freq = df['incident_location'].value_counts().to_dict()
    df['location_freq'] = df['incident_location'].apply(lambda x: dict_location_freq[x])
    df['Location Rank'] = df['location_freq'].rank( method = 'min' ,ascending = False)

    #side of town
    # checking for coordinates file presence
    if os.path.exists('resources/coordinates.pkl'):
        dict_cache_coordinates = unpickle_object('resources/coordinates.pkl')
    else:
        dict_cache_coordinates = {}
    
    geolocator = GoogleV3(api_key = "***REMOVED***")
    for address in df['incident_location'].unique():
        if address not in dict_cache_coordinates:
            dict_cache_coordinates[address] = get_coordinates(address, geolocator)

    pickle_object(dict_cache_coordinates, 'resources/coordinates.pkl')

    df['Side of Town'] = df['incident_location'].apply(lambda x: determine_side_of_town(dict_cache_coordinates[x]))

    # Incident rank - Nature field
    dict_nature_freq = df['nature'].value_counts().to_dict()
    df['nature_freq'] = df['nature'].apply(lambda x: dict_nature_freq[x])
    df['Incident Rank'] = df['nature_freq'].rank( method = 'min' ,ascending = False)

    #EMSSTAT flg

    #This is a boolean value that is True in two cases. First, 
    #if the Incident ORI was EMSSTAT or if the subsequent record or two contain an EMSSTAT at the same time and locaton.
    df['EMSSTAT'] = False
    df['EMSSTAT'] = df['incident_ori'].apply(lambda x: True if x == 'EMSSTAT' else False)
    df = df.reset_index().drop('index', axis = 1)

    for index in df[df['EMSSTAT'] == True].index:

        current_index_record =  df.loc[index]
        current_index_time = current_index_record['incident_time']
        current_index_location = current_index_record['incident_location']

        indices_to_check = [max(index-1, 0), max(index-2, 0), min(index+1, len(df)-1), min(index+2, len(df)-1)]

        for idx in indices_to_check:
            if df.loc[idx, 'incident_time'] == current_index_time and df.loc[idx, 'incident_location'] == current_index_location:
                df.loc[idx, 'EMSSTAT'] = True

    return df

    

        


    
