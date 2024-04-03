import pandas as pd
import urllib.request
from pypdf import PdfReader
import io
import pickle
import re
import logging


logger = logging.getLogger(__name__)


def download_pdf(url):
    """
    Function to download a PDF file from a given URL.

    Parameters:
    url (str): The URL of the PDF file to be downloaded.

    Returns:
    io.BytesIO: A BytesIO object containing the downloaded PDF file.

    Raises:
    urllib.error.URLError: If there is an error while opening the URL.
    """

    headers = {}
    headers["User-Agent"] = (
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    )
    data = io.BytesIO(
        urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
    )
    logger.info("Downloaded the PDF file")

    return data


def split_line_regex(line):
    """
    Split the line based on the regex pattern.

    Parameters:
    line (str): The input line to be split.

    Returns:
    list: A list of strings after splitting the line based on the regex pattern."""

    lst_str = re.split(r"\s{2,}", line)
    lst_str = [item.strip() for item in lst_str]
    return lst_str


def pdf_parser(pdf_stream):
    """
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
    - The PyPDF2 library is required to run this function."""

    PAGE_ONE = True
    EXPECTED_MIN_FIELDS = 3
    NUMBER_OF_JUNK_LINES = 3
    NUMBER_END_JUNK_LINES = 1
    FIELD_NAMES_ROW = 2

    lst_lines = []
    #pdf_file = PdfReader(pickle.load(open("filename", "rb")))
    pdf_file = PdfReader(pdf_stream)
    logger.info("Read the pdf byte stream")
    logger.debug("number of pages in the pdf {}".format(len(pdf_file.pages)))
    pdf_file.pages[0].extract_text()

    for page in pdf_file.pages:

        # extracting the context with layout method, the behavior can be truly unpredictable if the pdf format/structure changes
        page_extract = page.extract_text(
            extraction_mode="layout", layout_mode_space_vertically=False
        ).split("\n")

        if PAGE_ONE is True:

            # extracting the field names
            field_names = split_line_regex(page_extract[FIELD_NAMES_ROW])[1:]
            # removing the junk lines
            page_extract = page_extract[NUMBER_OF_JUNK_LINES:]
            PAGE_ONE = False

        # splitting the extracted line for respective field values
        lst_lines.extend([split_line_regex(item) for item in page_extract])

        # there might be some junk rows which might not have all the fields, so removing them
        # sometimes, the address over flows and recorded as new row, so removing them, its assumed only two fields go missing at once
        for item in lst_lines:
            if len(item) < EXPECTED_MIN_FIELDS:
                logger.debug("JUNK line {}".format(item))
        lst_lines = [item for item in lst_lines if len(item) >= EXPECTED_MIN_FIELDS]
    #lst_lines = lst_lines[:-NUMBER_END_JUNK_LINES]
    # creating the dataframe
    df = pd.DataFrame(lst_lines, columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori'])
    df['nature'] = df['nature'].apply(lambda x : '' if x is None else x )
    logger.debug("lines {}".format(lst_lines[0]))

    logger.debug("Number of records in dataframe {}".format(len(df)))

    # df.to_csv('resources/temp.csv')

    return df

def pickle_object(obj, file_path):

    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)

def unpickle_object(file_path):

    with open(file_path, 'rb') as file:
        obj = pickle.load(file)
    return obj

def get_coordinates(address, geolocator):
    location = geolocator.geocode(address, timeout = 10)
    if location is None:
        logger.error("Location not found for address {}".format(address))
        return ( -1000, -1000)
    return (location.latitude, location.longitude)

def determine_side_of_town(coord):

    center_lat = 35.220833
    center_lon = -97.443611

    if coord[0] == -1000:
        return 'Unknown'

    lat_diff = coord[0] - center_lat
    lon_diff = coord[1] - center_lon

    if lat_diff > 0:
        if lon_diff > 0:
            return 'NE'
        elif lon_diff < 0:
            return 'NW'
        else:
            return 'N'
    elif lat_diff < 0:
        if lon_diff > 0:
            return 'SE'
        elif lon_diff < 0:
            return 'SW'
        else:
            return 'S'
    else:
        if lon_diff > 0:
            return 'E'
        elif lon_diff < 0:
            return 'W'
        else:
            return 'Center'

# Example usage:
# latitude = 35.230833
# longitude = -97.433611
# side_of_town = determine_side_of_town(latitude, longitude)
# print(f"The side of town is {side_of_town}.")


