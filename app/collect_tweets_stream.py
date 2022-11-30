import os
import json
import time
import tenacity
from tenacity import retry,wait
import postgres
import requests
import pandas as pd
import tweepy
import re
import numpy as np
import base64
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

with open('credentials.json','r') as f:
    credential = json.load(f)

CONSUMER_KEY = credential['twitter_api_key']
CONSUMER_SECRET = credential['twitter_api_secret_key']
ACCESS_TOKEN = credential['twitter_access_token']
ACCESS_TOKEN_SECRET = credential['twitter_access_token_secret']
BEARER_TOKEN = credential['bearer_token']

query = 'IKEA lang:en -is:retweet'
tweet_fields = "tweet.fields=id,created_at,text,author_id"
emoji = re.compile('[\\u203C-\\u3299\\U0001F000-\\U0001F644]')
expansions = "expansions=author_id"
#headers = {"Authorization": "Bearer {}".format(bearer_token)}
def create_url(*params):
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields, expansions
    )
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "Subash"
    return r




#@retry(wait=wait_exponential(multiplier=900, min=2, max=30),  stop=stop_after_attempt(5))
#@tenacity.retry(wait=tenacity.wait_fixed(10) + wait.wait_random(0, 3))
def connect_to_endpoint(url):
    response1 = requests.request("GET", url, auth=bearer_oauth, stream=True)
    #print(response1.status_code)
    for response_line in response1.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            #t=json.dumps(json_response, indent=4, sort_keys=True)
            #columns=['id','created_at','text']
            for r in json_response['data']:
                user_id=r['author_id']
                i=r['id']
                created_at=r['created_at']
                text=r['text']
                rows = [ {"id":i,
                          "text":text,
                          "created_at":created_at}]
                f=list(filter(emoji.match,text))
                senti=sentimentAnalyse(text)
                #d=[(i,created_at,text)]
                #postgres.insert_tweet_data(i,text,created_at)
                #postgres.writetoPostgres(rows)
                postgres.writeTweets(user_id,i,text,senti,f,created_at)
                
                #d.append([id,created_at,text])
            #print(d)

    if response1.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response1.status_code, response1.text
            )
        )
        
def sentimentAnalyse(text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    senti=(max(vs, key=vs.get))
    return senti
    
    


def connectUrl():
    #Reformat the keys and encode them
    key_secret = '{}:{}'.format(CONSUMER_KEY, CONSUMER_SECRET).encode('ascii')
    #Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)
    #Transform from bytes back into Unicode
    b64_encoded_key = b64_encoded_key.decode('ascii')
    
    
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    print(auth_resp.status_code)
    access_token = auth_resp.json()['access_token']
    trend_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }
    
    trend_params = {
        'id': 1,
    }
    
    trend_url = 'https://api.twitter.com/1.1/trends/place.json'  
    return trend_params,trend_headers,trend_url

def extractData():
    trend_params,trend_headers,trend_url=connectUrl()
    trend_resp = requests.request("GET",trend_url, headers=trend_headers, params=trend_params,stream=True)
       #tweet_data = trend_resp.json()
    for response_line in trend_resp.iter_lines():
            if response_line:
               json_response = json.loads(response_line)
               for r in json_response:
                  try:
                     for i in (r['trends']):
                         trend_name=i['name']
                         url=i['url']
                         tweet_volume=i['tweet_volume']
                         postgres.writeTrends(trend_name,url,tweet_volume)
                  except TypeError:
                     print(f"TypeError :{json_response}")
               
                    
                    
    if trend_resp.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                trend_resp.status_code, trend_resp.text
            )
        )



def main():
    url = create_url(query, tweet_fields, expansions)
    timeout = 0
    while True:
        connect_to_endpoint(url)
        extractData()
        timeout += 1


if __name__ == "__main__":
    main()