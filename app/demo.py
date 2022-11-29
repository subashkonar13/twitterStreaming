import time
import random
import os
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine,text


db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
eng = create_engine(db_string)

def get_last_row():
    # Retrieve the last number inserted inside the 'numbers'
    query = "" + \
            "SELECT * " + \
            "FROM tweet_data " + \
            "WHERE IngestionTime >= (SELECT max(IngestionTime) FROM tweet_data)" +\
            "LIMIT 1"
    result_set = eng.execute(query)  
    for (r) in result_set:  
        return r[0]

if __name__ == '__main__':
    print('Application started')
    
    while True:
        time.sleep(1)
        print('The last value insterted is: {}'.format(get_last_row()))