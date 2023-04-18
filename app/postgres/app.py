import time
import random
import psycopg2
import json


with open('conf/credentials.json','r') as f:
    credentials = json.load(f)
db_user: str = credentials['db_user']
db_pass: str = credentials['db_pass']
db_host: str = credentials['db_host']
db_name: str = credentials['db_name']

    
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
