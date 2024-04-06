from datetime import timedelta, datetime
import os
import sqlite3
import pandas as pd
import requests_cache
from retry_requests import retry
import openmeteo_requests
import requests

class WeatherInfo:

    """
    class to get weather information for a given location and time
    """

    def __init__(self):

        if os.path.exists('resources/weather.db'):
            self.conn = sqlite3.connect('resources/weather.db')
        else:
            self.conn = sqlite3.connect('resources/weather.db')
            self.create_table()

    def create_table(self):
        # create a table to store weather information
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE weather (
                            coordinates TEXT,
                            date TEXT,
                            weather_code TEXT
                        )''')
        self.conn.commit()

    def populate_weather_info(self, coordinates, start_date, end_date):

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

        retry_session = retry(requests.Session(), retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

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
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}
        hourly_data["coordinates"] = "{}_{}".format(coordinates[0], coordinates[1])
        hourly_data["weather_code"] = hourly_weather_code
        hourly_dataframe = pd.DataFrame(data=hourly_data).dropna()
        hourly_dataframe["weather_code"] = hourly_dataframe["weather_code"].apply(lambda x : str(int(x)))
        hourly_dataframe['date'] = hourly_dataframe['date'].dt.strftime('%Y-%m-%d %H')

        # Save weather info to database
        hourly_dataframe.to_sql('weather', self.conn, if_exists='append', index=False)

        return None
    
    def get_weather_from_sqlite(self, coordinates, timestamp):
            
            """
            Retrieves the weather code for a given set of coordinates and timestamp.
    
            Parameters:
            - coordinates (tuple): A tuple containing the latitude and longitude coordinates.
            - timestamp (datetime): The timestamp for which the weather code is requested.
    
            Returns:
            - weather_code (str): The weather code corresponding to the given coordinates and timestamp.
    
            Note:
            - If the coordinates are (-1000, -1000), the function returns 'unknown'.
            - The weather code is retrieved from the database if available, otherwise it is fetched from an external source.
            """
    
            if coordinates[0] == -1000:
                return 'unknown'
    
            cursor = self.conn.cursor()
            cursor.execute("SELECT weather_code FROM weather WHERE coordinates = ? AND date = ?", ("{}_{}".format(coordinates[0], coordinates[1]),
                                                                                                    timestamp.strftime('%Y-%m-%d %H')))
            result = cursor.fetchone()
            if result is not None:
                return result[0]
    
            return None

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
        - The weather code is retrieved from the database if available, otherwise it is fetched from an external source.
        """

        if coordinates[0] == -1000:
            return 'unknown'

        coord_weather = self.get_weather_from_sqlite(coordinates, timestamp)
        if coord_weather is not None:
            #print("db hit")
            return coord_weather

        min_date = timestamp - timedelta(days=30)
        max_date = datetime.now()
        timestamp_str = timestamp.strftime('%Y-%m-%d %H')
        min_date_str = min_date.strftime('%Y-%m-%d')
        max_date_str = max_date.strftime('%Y-%m-%d')

        self.populate_weather_info(coordinates, min_date_str, max_date_str)

        # Save weather code to database
        return self.get_weather_from_sqlite(coordinates, timestamp)
    
    def close_connection(self):
        #closing database connection
        self.conn.close()
        return None