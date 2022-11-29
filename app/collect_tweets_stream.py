import os
import json
import time
import tenacity
from tenacity import retry,wait
import postgres
import requests
import pandas as pd
import postgres

with open('credentials.json','r') as f:
    credential = json.load(f)

CONSUMER_KEY = credential['twitter_api_key']
CONSUMER_SECRET = credential['twitter_api_secret_key']
ACCESS_TOKEN = credential['twitter_access_token']
ACCESS_TOKEN_SECRET = credential['twitter_access_token_secret']
BEARER_TOKEN = credential['bearer_token']


query = "IKEA"
tweet_fields = "tweet.fields=id,created_at,text"
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
                i=r['id']
                created_at=r['created_at']
                text=r['text']
                rows = [ {"id":i,
                          "text":text,
                          "created_at":created_at}]
                #d=[(i,created_at,text)]
                #postgres.insert_tweet_data(i,text,created_at)
                #postgres.writetoPostgres(rows)
                postgres.writePyscopg(i,text,created_at)
                #d.append([id,created_at,text])
            #print(d)

    if response1.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response1.status_code, response1.text
            )
        )



def main():
    url = create_url(query, tweet_fields, expansions)
    timeout = 0
    while True:
        connect_to_endpoint(url)
        timeout += 1


if __name__ == "__main__":
    main()
