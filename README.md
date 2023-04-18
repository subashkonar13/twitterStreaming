# Tutorial on Extracting data from twitter and feed it to Postgres after doing Sentimental Analysis

## Description
This tutorial is intended for self learning and making use of Twitter client authentication and consumer token(compatible with ver 2 and 1.1 respectively)

## Pre-requisites
1. Install Docker Desktop.
2. VSC/Any other interpreter.
3. Twitter Developer account with Elevated Access and necessary tokens generated.

## Modules
1. collect_tweet_stream.py extracts the tweets
2. app.py writes the data to postgres tables
3. Adminer  to view the data getting ingested
4. VADER analyses the sentiment

## Configuration
1. Make changes in the credentials.json to add the Twitter credentials.


## Execution

`docker compose up`
![alt text](https://github.com/subashkonar13/twitterStreaming/blob/main/images/git1.jpg)

## Monitor

Access the Adminer link- http://localhost:8080/?pgsql=db to watch the rows getting added.
