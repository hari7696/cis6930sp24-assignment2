from geopy.geocoders import GoogleV3
import pandas as pd
from assignment.utilities import determine_side_of_town, unpickle_object, pickle_object, get_coordinates
import os
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import timedelta, datetime
from tqdm import tqdm

import pandas as pd

def day_of_week(df):
    """
    Extracts the day of the week from the 'incident_time' column in the given DataFrame and returns the modified DataFrame.

    Parameters:
    - df (pandas.DataFrame): The input DataFrame containing the 'incident_time' column.

    Returns:
    - pandas.DataFrame: The modified DataFrame with an additional column 'Day of the Week' containing the corresponding day of the week as a numerical value.
    """

    df['Day of the Week'] = pd.to_datetime(df['incident_time'], format='%m/%d/%Y %H:%M').dt.day_name()
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

    return df

def time_of_day(df):
    """
    Extracts the hour of the day from the 'incident_time' column in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the 'incident_time' column.

    Returns:
        pandas.DataFrame: The DataFrame with an additional column 'Time of Day' containing the hour of the day.

    """
    df['Time of Day'] = pd.to_datetime(df['incident_time'], format = '%m/%d/%Y %H:%M' ).dt.hour
    return df



def location_rank(df):
    """
    Calculates the location rank based on the frequency of incident locations in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the incident data.

    Returns:
        pandas.DataFrame: The DataFrame with an additional column 'Location Rank' representing the rank of each location based on frequency.
    """

    dict_location_freq = df['incident_location'].value_counts().to_dict()
    df['location_freq'] = df['incident_location'].apply(lambda x: dict_location_freq[x])
    df['Location Rank'] = df['location_freq'].rank( method = 'min' ,ascending = False)

    return df


    ...
def geo_codes(df):

    """
    Retrieves and stores geocodes for incident locations in a DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing incident data.

    Returns:
        pandas.DataFrame: The DataFrame with an additional 'geocodes' column containing the geocodes for each incident location.

    """

    if os.path.exists('resources/coordinates.pkl'):
        dict_cache_coordinates = unpickle_object('resources/coordinates.pkl')
    else:
        dict_cache_coordinates = {}
    
    geolocator = GoogleV3(api_key = "AIzaSyA8yhHWkiTlSE39wKa8vvQxTafBDu3JdDQ")
    for address in df['incident_location'].unique():#tqdm(df['incident_location'].unique(), total = len(df['incident_location'].unique()), desc='Processing Coordinates'):
        if address not in dict_cache_coordinates:
            dict_cache_coordinates[address] = get_coordinates(address, geolocator)

    pickle_object(dict_cache_coordinates, 'resources/coordinates.pkl')

    df['geocodes'] = df['incident_location'].apply(lambda x:dict_cache_coordinates[x])

    return df


def incident_rank(df):

    """
    calculates the incident rank based on the frequency of incident nature in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the incident data.
    Returns:
        pandas.DataFrame: The DataFrame with an additional column 'Incident Rank' representing the rank of each incident nature based on frequency.
    """

    dict_nature_freq = df['nature'].value_counts().to_dict()
    df['nature_freq'] = df['nature'].apply(lambda x: dict_nature_freq[x])
    df['Incident Rank'] = df['nature_freq'].rank( method = 'min' ,ascending = False)

    return df

def emstat_flg(df):

    """
    Sets the 'EMSSTAT' flag to True for rows in the DataFrame where the 'incident_ori' column is 'EMSSTAT'.
    Additionally, it checks for records above and below each flagged row with matching incident time and location,
    and sets the 'EMSSTAT' flag to True for those records as well.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the 'incident_ori', 'incident_time', and 'incident_location' columns.

    Returns:
        pandas.DataFrame: The modified DataFrame with the 'EMSSTAT' flag updated.

    """
        
    df['EMSSTAT'] = False
    df['EMSSTAT'] = df['incident_ori'].apply(lambda x: True if x == 'EMSSTAT' else False)
    df = df.reset_index().drop('index', axis = 1)

    for index in df[df['EMSSTAT'] == True].index:

        current_index_record =  df.loc[index]
        current_index_time = current_index_record['incident_time']
        current_index_location = current_index_record['incident_location']

        indices_above = [max(index-1, 0), max(index-2, 0), min(index+1, len(df)-1), min(index+2, len(df)-1)]

        # checking for records above going till the start of the dataframe untill a mismatch is found
        for idx in range(index, -1, -1):
            if df.loc[idx, 'incident_time'] == current_index_time and df.loc[idx, 'incident_location'] == current_index_location:
                df.loc[idx, 'EMSSTAT'] = True
            else:
                break
        # check for records below, going till the end of the dataframe untill a mismatch is found
        for idx in range(index+1, len(df)):
            if df.loc[idx, 'incident_time'] == current_index_time and df.loc[idx, 'incident_location'] == current_index_location:
                df.loc[idx, 'EMSSTAT'] = True
            else:
                break


    return df

class WeatherInfo:

    """
    class to get weather information for a given location and time
    """

    def __init__(self):

        if os.path.exists('resources/weather.pkl'):
            self.dict_weather = unpickle_object('resources/weather.pkl')
        else:
            self.dict_weather = {}


    def get_weather_info(slef, coordinates, start_date, end_date):

        """
        Retrieves hourly weather information for a given location and time range.

        Args:
            coordinates (list): A list containing the latitude and longitude of the location.
            start_date (str): The start date of the time range in the format 'YYYY-MM-DD'.
            end_date (str): The end date of the time range in the format 'YYYY-MM-DD'.

        Returns:
            pandas.DataFrame: A DataFrame containing the hourly weather information, including the date and weather code.

        Raises:
            None

        Example:
            coordinates = [37.7749, -122.4194]
            start_date = '2022-01-01'
            end_date = '2022-01-31'
            weather_info = get_weather_info(coordinates, start_date, end_date)
        """

        cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": coordinates[0],
            "longitude": coordinates[1],
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "weather_code",
            "timezone": "America/Chicago"
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_weather_code = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["weather_code"] = hourly_weather_code
        hourly_dataframe = pd.DataFrame(data = hourly_data).dropna()
        hourly_dataframe['date'] = hourly_dataframe['date'].dt.strftime('%Y-%m-%d %H')

        return hourly_dataframe

    def get_weather_code(self, coordinates, timestamp):

        """
        Retrieves the weather code for a given set of coordinates and timestamp.

        Parameters:
        - coordinates (tuple): A tuple containing the latitude and longitude coordinates.
        - timestamp (datetime): The timestamp for which the weather code is requested.

        Returns:
        - weather_code (str): The weather code corresponding to the given coordinates and timestamp.

        Note:
        - If the coordinates are (-1000, -1000), the function returns 'unknown'.
        - The weather code is retrieved from a dictionary cache if available, otherwise it is fetched from an external source.
        """

        if coordinates[0] == -1000:
            return 'unkown'

        min_date = timestamp - timedelta(days = 180)
        max_date = datetime.now()
        #timestamp = timestamp.strftime('%Y-%m-%d %H')
        timestamp_str = timestamp.strftime('%Y-%m-%d %H')

        min_date_str = min_date.strftime('%Y-%m-%d')
        max_date_str = max_date.strftime('%Y-%m-%d')

        key = "{}_{}".format(coordinates[0], coordinates[1])
        
    
        if key in self.dict_weather:
            temp_df = self.dict_weather[key]
            weather_code = temp_df[temp_df['date'] == timestamp_str]['weather_code'].values[0]

        else:
            temp_df = self.get_weather_info(coordinates, min_date_str, max_date_str)
            self.dict_weather[key] = temp_df
            weather_code = temp_df[temp_df['date'] == timestamp_str]['weather_code'].values[0]

        return weather_code    
    
    def save_weather_info(self):
        pickle_object(self.dict_weather, 'resources/weather.pkl')



def extract_feilds(df):

    """
    Extracts various fields from the input DataFrame and returns a modified DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the data to be processed.

    Returns:
    pandas.DataFrame: The modified DataFrame with additional fields extracted.

    """
    
    #day of week extraction
    df = day_of_week(df)

    #time of the day extraction
    df = time_of_day(df)

    #Location Rank
    df = location_rank(df)

    #side of town
    # checking for coordinates file presence
    df = geo_codes(df)
    df['Side of Town'] = df['geocodes'].apply(lambda x: determine_side_of_town(x))

    # Incident rank - Nature field
    df = incident_rank(df)

    #EMSSTAT flg
    df = emstat_flg(df)

    #weather codes

    weather_obj = WeatherInfo()
    df['incident_time'] = pd.to_datetime(df['incident_time'], format = '%m/%d/%Y %H:%M')
    df['Weather'] = ''

    for index, row in df.iterrows():#tqdm(df.iterrows(), total=df.shape[0], desc='Processing Weather'):
        df.at[index, 'Weather'] = weather_obj.get_weather_code(row['geocodes'], row['incident_time'])
    weather_obj.save_weather_info()

    df.to_csv("final_out.csv", index = False)

    df = df[['Day of the Week', 'Time of Day', 'Weather', 'Location Rank', 'Side of Town', 'Incident Rank', 'Nature', 'EMSSTAT']]

    return df

    

        


    
