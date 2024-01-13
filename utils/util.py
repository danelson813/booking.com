# utils/util.py
import logging
import os.path
import pandas as pd
import sqlite3 as sql


def setup_logger():
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("data/info.log", 'w')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(pathname)s - %(lineno)d | %(levelname)s: %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def does_it_exist(filename: str) -> bool:
    path = filename
    check_file = os.path.isfile(path)
    return check_file


def dataframe(results: list) -> 'pd.core.frame.DataFrame':
    df = pd.DataFrame(results)
    df.to_csv("data/results.csv", index=False)
    return df


def to_sqlite3(df: 'pd.core.frame.DataFrame'):
    conn = sql.connect('data/booking.sqlite')
    # write tdhe new DataFrame to a new SQLite table
    df.to_sql("lodging", conn, if_exists='replace')
    conn.close()

def read_the_csv(filename: str) -> 'pd.core.frame.DataFrame':
    df_from_csv = pd.read_csv(filename)
    return df_from_csv

def data_cleaning(df: 'pd.core.frame.DataFrame') -> 'pd.core.frame.DataFrame':
    logger = setup_logger()
    logger.info("Cleaning the dataframe")
    # df = df.drop_duplicates(inplace=True)

    df['rating'] = df['rating'].astype("float")
    df['price'] = df['price'].astype("int32")
    df['#reviews'] = df['#reviews'].astype('int32')
    return df

def view():
  new_data = sql.connect('data/booking.sqlite')
  change = new_data.cursor()
  change.execute("SELECT * FROM lodging")
  rows = change.fetchall()
  change.close()
  return rows



if __name__ == '__main__':
    print("You have run the wrong file")
