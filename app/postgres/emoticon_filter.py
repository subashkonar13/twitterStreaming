import os
import json
import time
import tenacity
from tenacity import retry,wait
import postgres
import requests
import pandas as pd
#import postgres
import re


def writetoemoticon(*params):
    try:
       connection = psycopg2.connect(user=db_user,
                                  password=db_pass,
                                  host=db_host,
                                  port=db_port,
                                  database=db_name)
       cursor = connection.cursor()
       postgres_insert_query = """ INSERT INTO Emoticon_Data (id, f, created_at) VALUES (%s,%s,%s)"""
       #record_to_insert = (i, text, created_at)
       record_to_insert = (params)
       cursor.execute(postgres_insert_query, record_to_insert)
       connection.commit()
       count = cursor.rowcount
       print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
       print("Failed to insert record into mobile table", error)

