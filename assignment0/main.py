from utilities import *
from field_extractor import *
from db_components import *
import argparse


def main(url):
    """
    Downloads a PDF file from the given URL, parses it, creates a database, populates the database with data from the PDF,
    executes a query on the database, and prints the query results.

    Parameters:
    url (str): The URL of the PDF file to download.

    Returns:
    None
    """

    # downloading the pdf file
    pdf_byte_stream = download_pdf(url)
    logging.info("Downloaded the pdf file")

    # parsing the pdf file
    df = pdf_parser(pdf_byte_stream)
    df.to_pickle("tests/assignment0.pkl")
    df_enhanced = extract_feilds(df)
    df_enhanced.to_csv("tests/assignment0.csv", index = False)
    # logging.info("Parsed the pdf file")

    # # creating the database
    # conn = createdb()
    # logging.info("Created the database")

    # create_table(conn)
    # logging.info("Created the table")

    # # populating the database
    # populate_db(conn, df)
    # logging.info("Populated the database")
    # conn.commit()

    # # querying db
    # query = """SELECT nature, count(*) as num_incidents FROM incidents GROUP BY nature ORDER BY num_incidents DESC, nature NULLS first"""

    # query_output = query_db(conn, query)
    # logging.info("Query run successfully")

    # FLAG =False
    # # printing the query results
    # for row in query_output:
    #     print("|".join(map(str, row)))

    
# if row[0] == '':
#     store_string = temp_string
#     FLAG = True
# else:
            

    # if FLAG:
    #     print(store_string)
    #     logging.debug("store string {}".format(store_string))
    # conn.close()
    # logging.info("Closed the database connection")


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
        "--incidents", type=str, required=True, help="Incident summary url."
    )

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)


# run command: pipenv run python assignment0/main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-01_daily_incident_summary.pdf"