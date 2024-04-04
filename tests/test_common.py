import pytest
import sys
import os.path
import pandas as pd
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from assignment.utilities import download_pdf, split_line_regex, pdf_parser
from assignment.field_extractor import day_of_week, time_of_day, location_rank, geo_codes, incident_rank, emstat_flg, WeatherInfo


# def test_download_pdf_and_pdf_parser():
#     url = "https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-01_daily_incident_summary.pdf"
#     pdf_stream = download_pdf(url)
#     df = pdf_parser(pdf_stream)
#     assert len(df) > 0


def test_split_line_regex():
    """
    Test case for the split_line_regex function.

    This test case verifies that the split_line_regex function correctly splits a line of text using a regular expression.

    The line used for testing is:
    "12/31/2023 00:00:00         2023-00000001       100 Blk W Boyd St      Traffic Stop         OK0140200"

    The expected output is a list containing the following elements:
    [
        "12/31/2023 00:00:00",
        "2023-00000001",
        "100 Blk W Boyd St",
        "Traffic Stop",
        "OK0140200",
    ]
    """
    line = "12/31/2023 00:00:00         2023-00000001       100 Blk W Boyd St      Traffic Stop         OK0140200"
    lst_str = split_line_regex(line)
    assert lst_str == [
        "12/31/2023 00:00:00",
        "2023-00000001",
        "100 Blk W Boyd St",
        "Traffic Stop",
        "OK0140200",
    ]

def test_day_of_week():
    """
    Test case for the day_of_week function.

    This test case verifies that the day_of_week function correctly extracts the day of the week from a given date string.

    The date string used for testing is "12/31/2023", which corresponds to a Wednesday.

    The expected output is "Wednesday".
    """

    date_str = "12/31/2023 10:00"
    df = pd.DataFrame({"incident_time": [date_str]})
    df_out = day_of_week(df)
    assert  df_out['Day of the Week'].values[0] == 1 # sunday

def test_time_of_day():
    """
    Test case for the time_of_day function.

    This test case verifies that the time_of_day function correctly extracts the time of day from a given time string.

    The time string used for testing is "12/31/2023 10:00", which corresponds to 10:00 AM.

    The expected output is "Morning".
    """

    date_str = "12/31/2023 10:00"
    df = pd.DataFrame({"incident_time": [date_str]})
    df_out = time_of_day(df)
    assert  df_out['Time of Day'].values[0] == 10

def test_location_rank():

    """
    Test case for the location_rank function.

    This test case verifies that the location_rank function

    The ranks should be based on the frequency of the location in the dataset. 
    The most frequent location should have a rank of 1, 
    the second most frequent location should have a rank of 2, and so on.
    """

    df = pd.DataFrame(['A', 'A', 'A', 'B', 'B', 'C'], columns = ['incident_location'])
    df_out = location_rank(df)
    assert  list(df_out['Location Rank'].values) == [1,1,1,4,4,6]

def test_geo_codes():
    """
    Test case for the geo_codes function.

    This test case verifies that the geo_codes function correctly extracts the latitude and longitude coordinates for a given address.

    The address used for testing is "12TH AVE NE / SONOMA PARK DR".

    The expected output is a tuple containing the latitude and longitude coordinates of the address.
    """

    address = "12TH AVE NE / SONOMA PARK DR"
    df = pd.DataFrame({"incident_location": [address]})
    df_out = geo_codes(df)
    assert  df_out['geocodes'].values[0][0] == 35.23 and df_out['geocodes'].values[0][1] == -97.4235

def test_incident_rank():
    """
    Test case for the incident_rank function.

    This test case verifies that the incident_rank function correctly assigns a rank to each Nature based on the frequency of the Nature in the dataset."""

    df = pd.DataFrame(['A', 'A', 'A', 'B', 'B', 'C'], columns = ['nature'])
    df_out = incident_rank(df)
    assert  list(df_out['Incident Rank'].values) == [1.0, 1.0, 1.0, 4.0, 4.0, 6.0]


def test_emstat_flag():

    """
    Test case for the emstat_flg function.

    This test case verifies that the emstat_flg function correctly assigns a flag

    """

    df = pd.DataFrame({'incident_location':['A','A','A','A'],
                       'incident_time':['12/31/2023 10:00','12/31/2023 10:00',
                                        '12/31/2023 10:00','12/31/2023 10:00'],
                       'incident_ori':['OK0140200', 'OK0140200', 'EMSSTAT', 'OK0140200']})
    
    df_out = emstat_flg(df)
    assert  list(df_out['EMSSTAT'].values) == [True, True, True, True]

def test_weather_info():

    """
    Test case for the WeatherInfo class.
    It hits the weather api and returns the weather code for the given location and time."""

    weather_obj = WeatherInfo()
    assert weather_obj.get_weather_code((35.1816, -97.4143), pd.to_datetime('2024-03-01 12')) == 0