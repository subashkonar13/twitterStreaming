import os
import json
import time
import tenacity
from tenacity import *
import postgres
import requests
import pandas as pd
import tweepy
import re
import numpy as np
import base64
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List,Dict, Any, Tuple
import base64
import requests

# Define constants
with open('conf/credentials.json','r') as f:
    credentials = json.load(f)

CONSUMER_KEY: str = credentials['twitter_api_key']
CONSUMER_SECRET: str = credentials['twitter_api_secret_key']
ACCESS_TOKEN: str = credentials['twitter_access_token']
ACCESS_TOKEN_SECRET: str = credentials['twitter_access_token_secret']
BEARER_TOKEN: str = credentials['bearer_token']
QUERY: str = 'IPL lang:en -is:retweet'
TWEET_FIELDS: str = "tweet.fields=id,created_at,text,author_id"
EMOJI_REGEX: re.Pattern = re.compile('[\\u203C-\\u3299\\U0001F000-\\U0001F644]')
EXPANSIONS: str = "expansions=author_id"

def create_url(query: str, tweet_fields: str, expansions: str) -> str:
    """
    Constructs the search URL for the Twitter API given the query, tweet fields, and expansions.

    Args:
    - query (str): The search query to use for the API.
    - tweet_fields (str): The tweet fields to include in the API response.
    - expansions (str): The expansions to include in the API response.

    Returns:
    - str: The constructed search URL.
    """
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





@retry(wait=wait_exponential(min=2, max=60), stop=stop_after_attempt(5))
def connect_to_endpoint(url: str) -> None:
    """
    Connects to the given endpoint URL and writes the tweets data to Postgres.
    """
    response1 = requests.get(url, auth=bearer_oauth, stream=True)
    if response1.status_code != 200:
        """Raise an exception if the response is not 200 (OK)
        """
        raise Exception(f"Request returned an error: {response1.status_code} {response1.text}")
    for response_line in response1.iter_lines():
        if not response_line:
            continue
        json_response = json.loads(response_line)
        for tweet in json_response.get('data', []):
            user_id = tweet['author_id']
            tweet_id = tweet['id']
            created_at = tweet['created_at']
            text = tweet['text']
            emojis = list(filter(EMOJI_REGEX.match, text))
            sentiment, comp = sentiment_analyze(text)
            if sentiment=='neu':
                    sentiment='Neutral'
            elif sentiment=='pos':
                    sentiment='Positive'
            elif sentiment=='neg':
                    sentiment='Negative'
            elif sentiment=='compound':
                    sentiment='Mixed feelings'
            else:
                    sentiment='Not available'
            postgres.writeTweets(user_id, tweet_id, text, sentiment, comp, emojis, created_at)

    if response1.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response1.status_code, response1.text
            )
        )

        
def sentiment_analyze(text: str) -> Tuple[str, float]:
    """
    Analyzes the sentiment of the given text and returns the dominant sentiment and compound score.
    """
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    sentiment = max(vs, key=vs.get)
    comp = vs['compound']
    return sentiment, comp

 
    




def connectUrl() -> Tuple[Dict[str, Any], Dict[str, str], str]:
    """Connect to Twitter API and get authorization headers and URL parameters for trends API.

    Returns:
        A tuple containing the URL parameters, authorization headers, and URL for trends API.
    """
    key_secret = f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret).decode('ascii')
    base_url = 'https://api.twitter.com/'
    auth_url = f"{base_url}oauth2/token"
    auth_headers = {
        "Authorization": f"Basic {b64_encoded_key}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }
    auth_data = {"grant_type": "client_credentials"}
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    access_token = auth_resp.json()["access_token"]
    trend_headers = {"Authorization": f"Bearer {access_token}"}
    trend_params = {"id": 1}
    trend_url = f"{base_url}1.1/trends/place.json"
    return trend_params, trend_headers, trend_url



def extractData() -> None:
    """
    Extracts data from Twitter API and writes it to the database.

    Raises:
        Exception: If the request returns an error.
    """
    trend_params, trend_headers, trend_url = connectUrl()
    trend_resp = requests.request("GET", trend_url, headers=trend_headers, params=trend_params, stream=True)

    for response_line in trend_resp.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            for r in json_response:
                try:
                    for i in r['trends']:
                        trend_name = i['name']
                        url = i['url']
                        tweet_volume = i.get('tweet_volume', None)
                        postgres.writeTrends(trend_name, url, tweet_volume)
                except TypeError:
                    print(f"TypeError: {json_response}")

    if trend_resp.status_code != 200:
        raise Exception(
            f"Request returned an error: {trend_resp.status_code} {trend_resp.text}"
        )



def main() -> None:
    """
    Run the main program loop.

    Returns:
        None
    """
    url: str = create_url(QUERY, TWEET_FIELDS, EXPANSIONS)
    timeout: int = 0
    while True:
        connect_to_endpoint(url)
        extractData()
        timeout += 1


if __name__ == "__main__":
    main()
