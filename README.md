# cis6930sp24-assignment2

The project is about parsing the pdf files and enhancing the the extracted the fields by performing the augmentation on them.

### Project Implementation Steps.
1. Download all the pdf files present in the given csv file
2. Parse the pdf and extract the fields
3. Augment the fields
4. Write the augmented fields to output

### Expected outcome
1. A reliable augmented data written to stdout

### Data Handling.

1. During the data augmentation for some address, the geocoding is failed to provide any cooordinates, so those are filled with 'unkown' strings
Other fields like 'Side of Town' and 'Day of the Week' rely on these geocoding, so they are too filled with 'unkown' value
2. The geo-coordinates are rounded off to 4 decimals, thus giving the location accuracy of 11 meters.
3. The ranking for the fields 'Location Rank' and 'Incident Rank' are actually based on the frequency of them in the respective pdf file

### Environment setup
Run the follwing pipenv command to create the required environment

```pipenv install```

### How to run

```pipenv install```

```pipenv run python .\assignment2.py --urls files.csv```




https://github.com/hari7696/cis6930sp24-assignment2/assets/148893192/40dbd0fc-48a3-4ded-bb48-2d5eeb72af8b



### Test cases run

The test doesnt need any explicit inputs, running following pipenv command run the pytest cases. The project have 6 test cases.

```pipenv run python -m pytest```

## Functions

### main()
    
    Downloads and parses PDF files from a list of URLs, extracts fields, and writes the results to stdout.

    Parameters:
    - file (str): The path to the CSV file containing the list of URLs.

    Returns:
    Noneone

### day_of_week()
    Extracts the day of the week from the 'incident_time' column in the given DataFrame and returns the modified DataFrame.

    Parameters:
    - df (pandas.DataFrame): The input DataFrame containing the 'incident_time' column.

    Returns:
    - pandas.DataFrame: The modified DataFrame with an additional column 'Day of the Week' containing the corresponding day of the week as a numerical value.
    
#### time_of_day():
    Extracts the hour of the day from the 'incident_time' column in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the 'incident_time' column.

    Returns:
        pandas.DataFrame: The DataFrame with an additional column 'Time of Day' containing the hour of the day.


#### location_rank():
    Calculates the location rank based on the frequency of incident locations in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the incident data.

    Returns:
        pandas.DataFrame: The DataFrame with an additional column 'Location Rank' representing the rank of each location based on frequency.

#### geo_codes():

    Retrieves and stores geocodes for incident locations in a DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing incident data.

    Returns:
        pandas.DataFrame: The DataFrame with an additional 'geocodes' column containing the geocodes for each incident location.


#### incident_rank():

    calculates the incident rank based on the frequency of incident nature in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the incident data.
    Returns:
        pandas.DataFrame: The DataFrame with an additional column 'Incident Rank' representing the rank of each incident nature based on frequency.

#### emstat_flg():

    Sets the 'EMSSTAT' flag to True for rows in the DataFrame where the 'incident_ori' column is 'EMSSTAT'.
    Additionally, it checks for records above and below each flagged row with matching incident time and location,
    and sets the 'EMSSTAT' flag to True for those records as well.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the 'incident_ori', 'incident_time', and 'incident_location' columns.

    Returns:
        pandas.DataFrame: The modified DataFrame with the 'EMSSTAT' flag updated.



#### populate_weather_info():

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

#### get_weather_from_sqlite():

    Retrieves the weather code for a given set of coordinates and timestamp.

    Parameters:
    - coordinates (tuple): A tuple containing the latitude and longitude coordinates.
    - timestamp (datetime): The timestamp for which the weather code is requested.

    Returns:
    - weather_code (str): The weather code corresponding to the given coordinates and timestamp.

    Note:
    - If the coordinates are (-1000, -1000), the function returns 'unknown'.
    - The weather code is retrieved from the database if available, otherwise it is fetched from an external source.

#### get_weather_code()

    Retrieves the weather code for a given set of coordinates and timestamp.

    Parameters:
    - coordinates (tuple): A tuple containing the latitude and longitude coordinates.
    - timestamp (datetime): The timestamp for which the weather code is requested.

    Returns:
    - weather_code (str): The weather code corresponding to the given coordinates and timestamp.

    Note:
    - If the coordinates are (-1000, -1000), the function returns 'unknown'.
    - The weather code is retrieved from the database if available, otherwise it is fetched from an external source.
        
            


#### extract_feilds():

    Extracts various fields from the input DataFrame and returns a modified DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the data to be processed.

    Returns:
    pandas.DataFrame: The modified DataFrame with additional fields extracted.


#### download_pdf():
    Function to download a PDF file from a given URL.

    Parameters:
    url (str): The URL of the PDF file to be downloaded.

    Returns:
    io.BytesIO: A BytesIO object containing the downloaded PDF file.

    Raises:
    urllib.error.URLError: If there is an error while opening the URL.

#### split_line_regex():
    Split the line based on the regex pattern.

    Parameters:
    line (str): The input line to be split.

    Returns:
    list: A list of strings after splitting the line based on the regex patter

#### pdf_parser():
    Function to parse the pdf file and return the dataframe.

    Parameters:
    pdf_stream (bytes): The byte stream of the PDF file.

    Returns:
    pandas.DataFrame: The parsed data as a DataFrame.

    Details:
    This function takes a byte stream of a PDF file and extracts the data from it. It assumes that the PDF file
    has a specific structure with field names in a certain row and a fixed number of fields per row. The function
    uses the PyPDF library to read the PDF file and extract the text from each page. It then splits the extracted
    text into lines and processes each line to extract the field values. Junk lines that do not have the expected
    number of fields are removed. Finally, the extracted data is converted into a pandas DataFrame and returned.

    Note:
    - The behavior of this function can be unpredictable if the PDF format/structure changes.
    - The PyPDF2 library is required to run this functio

#### get_coordinates():
Get the latitude and longitude coordinates for a given address using a geolocator.

    Args:
        address (str): The address to geocode.
        geolocator: The geolocator object used for geocoding.

    Returns:
        tuple: A tuple containing the latitude and longitude coordinates of the address.    


#### determine_side_of_town():
Determine the side of town based on the latitude and longitude coordinate

### test functions

#### test_split_line_regex():
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

#### test_day_of_week():
    Test case for the day_of_week function.

    This test case verifies that the day_of_week function correctly extracts the day of the week from a given date string.

    The date string used for testing is "12/31/2023", which corresponds to a Wednesday.

    The expected output is "Wednesday".


#### test_time_of_day():
    Test case for the time_of_day function.

    This test case verifies that the time_of_day function correctly extracts the time of day from a given time string.

    The time string used for testing is "12/31/2023 10:00", which corresponds to 10:00 AM.

    The expected output is "Morning".

#### test_location_rank():

    Test case for the location_rank function.

    This test case verifies that the location_rank function

    The ranks should be based on the frequency of the location in the dataset. 
    The most frequent location should have a rank of 1, 
    the second most frequent location should have a rank of 2, and so on.

#### test_geo_codes():
    Test case for the geo_codes function.

    This test case verifies that the geo_codes function correctly extracts the latitude and longitude coordinates for a given address.

    The address used for testing is "12TH AVE NE / SONOMA PARK DR".

    The expected output is a tuple containing the latitude and longitude coordinates of the address.

#### test_incident_rank():
    Test case for the incident_rank function.

    This test case verifies that the incident_rank function correctly assigns a rank to each Nature based on the frequency of the Nature in the datase

#### test_emstat_flag():

    Test case for the emstat_flg function.

    This test case verifies that the emstat_flg function correctly assigns a flag



#### test_weather_info():

    Test case for the WeatherInfo class.
    It hits the weather api and returns the weather code for the given location and time

## Bugs and Assumption
1. Bugs: the code uses two apis, open meteo and google geocoding api. if the api calls limit or rate exceeds, the code may fail to run
2. Extracting data pdf is really complicated, so if the structure of the changes from the given incident file, the behaviour od the code can be unpredicatable, it may even break
3. For the expected outcome, its assumed that the structure of the pdf file remains same as given in assignment
4. Assumption: The code should have write access to the resources directory
5. Asuumption: the first 2 rows of the pdf is junk data, so it gets removed everytime
6. The last row of the pdf have a time stamp, so its ignroed as junk value
