import time
import random
from sqlalchemy import create_engine,text
import pyspark
import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql import Row
db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

'''
def insert_tweet_data(i,text,created_at):
    # Insert a new number into the 'numbers' table.
    #id=id,
    #tweet_text=text,
    #created_at=created_at  
    #db.execute("INSERT INTO Tweet_Data(id,tweet_text,created_at) VALUES (:id,:tweet_text,:created_at)",{"id":i,"tweet_text":text,"created_at":created_at})
    query=  "INSERT INTO Tweet_Data(id,tweet_text,created_at) VALUES (:id,:tweet_text,:created_at)"  
    db.execute(text(query),{"id":i,"tweet_text":text,"created_at":created_at})
 
def writetoPostgres(rows):
    #rdd=spark.sparkContext.parallelize([t])
    #df=spark.createDataFrame(d)
    #df1 = spark.read.option("multiline","true").json(rdd)    
    #df=df1.select('id','text','created_at')
    df=spark.createDataFrame(rows)
    df.write.format("jdbc")\
    .option("url", "jdbc:postgresql://db:5432/database") \
    .option("driver", "org.postgresql.Driver").option("dbtable", "tweet_data") \
    .option("user", "username").option("password", "secret").save()
'''    
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
       tweet_query = """ INSERT INTO Tweet_Data (user_id,tweet_id, tweet_text,sentiment,Emoticon,created_at) VALUES (%s,%s,%s,%s,%s,%s)"""
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
'''
if __name__ == '__main__':
    print('Application started')
    
    while True:
        time.sleep(1)
        #insert_tweet_data(random.randint(1,1000000),id,text,created_at)
        #print('The last value insterted is: {}'.format(get_last_row()))
'''