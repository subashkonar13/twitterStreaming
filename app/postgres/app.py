import time
import random
#from sqlalchemy import create_engine,text
#import pyspark
import psycopg2
import json


def connect_db() -> tuple:
    """
    Connects to the database using the credentials in the "conf/credentials.json" file.

    Returns:
        A tuple containing the cursor and connection objects.
    """
    try:
        with open('conf/credentials.json', 'r') as f:
            credentials = json.load(f)
        db_user:str = credentials['db_user']
        db_pass:str = credentials['db_pass']
        db_host:str = credentials['db_host']
        db_port:str = credentials['db_port']
        db_name:str = credentials['db_name']
        connection = psycopg2.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name
        )
        cursor = connection.cursor()
        return cursor, connection
    except (Exception, psycopg2.Error) as error:
        print("Failed to establish connection", error)

def write_tweets(*params: tuple) -> None:
    """
    Inserts a new record into the "Tweet_Data" table.

    Args:
        *params: A tuple containing the values to be inserted into the table.

    Returns:
        None
    """
    try:
        cursor, connection = connect_db()
        tweet_query = """INSERT INTO Tweet_Data (user_id, tweet_id, tweet_text, sentiment, comp, Emoticon, created_at)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(tweet_query, params)
        connection.commit()
        print("Record inserted successfully into table")
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into Tweet_Data table", error)

       
def write_trends(*p: tuple) -> None:
    """
    Insert trending data into the Trending_Data table.

    Args:
    *params: tuple: A tuple of trending data to be inserted.

    Returns:
    None
    """
    try:
        cursor, connection = connect_db()
        trending_query = """ INSERT INTO Trending_Data (trend_name, url, tweet_volume) VALUES (%s, %s, %s)"""
        cursor.execute(trending_query, p)
        connection.commit()
        print("Record inserted successfully into table")
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into Trending_Data table", error)    
