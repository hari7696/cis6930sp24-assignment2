import sqlite3
import os
import logging

logger = logging.getLogger(__name__)


def createdb():
    """
    Creates a new SQLite database and returns a connection object.

    Returns:
        conn (sqlite3.Connection): Connection object representing the newly created database.
    """
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    logger.debug(" Database Absolute path {}".format(abs_path))

    if os.path.exists(os.path.join(abs_path, "resources")):
        logger.debug("resources folder exists")
    else:
        os.mkdir(os.path.join(abs_path, "resources"))
        logger.debug("resources folder created")

    # Checking if there is an existing db
    if os.path.exists(os.path.join(abs_path, "resources", "normanpd.db")):
        os.remove(os.path.join(abs_path, "resources", "normanpd.db"))
        logger.debug("Removed the existing db")

    conn = sqlite3.connect(os.path.join(abs_path, "resources", "normanpd.db"))
    logger.info("Created the db")
    return conn


def create_table(conn):
    """
    Creates a table named 'incidents' in the database.

    Parameters:
    conn (Connection): The database connection object.

    Returns:
    None
    """

    conn.execute(
        """CREATE TABLE incidents (
                    incident_time TEXT,
                    incident_number TEXT,
                    incident_location TEXT,
                    nature TEXT,
                    incident_ori TEXT
                );"""
    )
    logger.info("table creation successful")


def populate_db(conn, df):
    """
    Populates the database with data from a DataFrame.

    Parameters:
    conn (Connection): The database connection object.
    df (DataFrame): The DataFrame containing the data to be inserted into the database.

    Returns:
    None

    Details:
    - Renames the columns of the DataFrame to ['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori'].
    - Inserts the data from the DataFrame into the 'incidents' table in the database.
    - If the 'incidents' table already exists, the data is appended to it.
    - Logs a debug message with the column names of the DataFrame.
    - Logs an info message indicating that the database has been populated.
    """
    df.columns = [
        "incident_time",
        "incident_number",
        "incident_location",
        "nature",
        "incident_ori",
    ]
    logger.debug("columns names {}".format(df.columns))
    df.to_sql("incidents", conn, if_exists="append", index=False)
    logger.info("Populated the db")


def query_db(conn, query):
    """
    Execute a database query.

    Parameters:
    conn (connection): The database connection object.
    query (str): The SQL query to be executed.

    Returns:
    result (object): The result of the query execution.
    """
    return conn.execute(query)
