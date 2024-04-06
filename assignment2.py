from assignment.utilities import *
from assignment.field_extractor import *
import argparse
import pandas as pd
import sys

def main(file):
    """
    Downloads and parses PDF files from a list of URLs, extracts fields, and writes the results to stdout.

    Parameters:
    - file (str): The path to the CSV file containing the list of URLs.

    Returns:
    None
    """

    lst_urls = list(pd.read_csv(file, header=None)[0].values)

    lst_df_holder = []

    for url in lst_urls:

        pdf_byte_stream = download_pdf(url)
        logging.info("Downloaded the pdf file")
        # parsing the pdf file
        df = pdf_parser(pdf_byte_stream)
        logging.info("Parsed the pdf file , {}, url: {}".format(df.shape, url))
        # df.to_pickle("tests/assignment0.pkl")
        df_enhanced = extract_feilds(df)
        logging.info("Extracted the fields from pdf file , {}, url: {}".format(df_enhanced.shape, url))
        # df_enhanced.to_csv("tests/assignment0.csv", index = False)
        lst_df_holder.append(df_enhanced)

    df_final = pd.concat(lst_df_holder, axis = 0)

    sys.stdout.write("\t".join(df_final.columns) + "\n")

    for row in df_final.iterrows():
        sys.stdout.write("\t".join(map(str,row[1].values)) + "\n")



if __name__ == "__main__":

    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        filename="tests/assignment0.log",
        filemode="w",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--urls", type=str, required=True, help="file with list of urls to parse"
    )

    args = parser.parse_args()
    if args.urls:
        main(args.urls)


# run command: pipenv run python assignment0/main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-01_daily_incident_summary.pdf"
#https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-02_daily_incident_summary.pdf
# pipenv run python .\assignment2.py --urls files.csv