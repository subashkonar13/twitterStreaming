import time
import random
from sqlalchemy import create_engine,text
#import pyspark
import psycopg2
db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)
    
def connectdb():
   try:
       connection = psycopg2.connect(user=db_user,
                                  password=db_pass,
                                  host=db_host,
                                  port=db_port,
                                  database=db_name)
       cursor = connection.cursor()
       return cursor,connection
   except (Exception, psycopg2.Error) as error:
       print("Failed to establish Connection", error)
    
    
#def writePyscopg(i,text,created_at):
def writeTweets(*params):
    try:
       cursor,connection=connectdb()
       tweet_query = """ INSERT INTO Tweet_Data (user_id,tweet_id, tweet_text,sentiment,comp,Emoticon,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
       tweet_to_insert = (params)
       cursor.execute(tweet_query, tweet_to_insert)
       connection.commit()
       #count = cursor.rowcount
       print("Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
       print("Failed to insert record into Tweet_Data table", error)

       
def writeTrends(*p):
    try:
       cursor,connection=connectdb()
       trending_query = """ INSERT INTO Trending_Data (trend_name, url, tweet_volume) VALUES (%s,%s,%s)"""
       trend_to_insert = (p)
       cursor.execute(trending_query, trend_to_insert)
       connection.commit()
       #count = cursor.rowcount
       print("Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
       print("Failed to insert record into Trending_Data table", error)      
