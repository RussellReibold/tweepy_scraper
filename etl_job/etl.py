'''
Python module that

1) Extracts Data From the MongoDB database
- Connect to the database
- Query the data

2) Transforms the data
- Maybe we will need to convert the data into a different datatype? (In this case not)
- Perform sentiment analysis

3) Loads the data into a Postgres database
- Connect to the database
- Create table(s)
- INSERT INTO
'''

import time
import logging

from pymongo import MongoClient
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

time.sleep(20)

# Connect to the MongoDB database
client = MongoClient(host=config.hostmongo, port=config.portmongo)
mongo_db = client.twitter_pipeline
tweet_collection = mongo_db.tweets

# Connect to the Postgres database
HOST = config.HOSTPOST
USERNAME = config.USERNAME
PORT = config.PORTPOST
DB = config.DB
PASSWORD = config.PASSWORD

engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}', pool_size=50, max_overflow=100)

# Create table tweets in the Postgres database
CREATE_QUERY = ''' CREATE TABLE IF NOT EXISTS tweets
                   (id SERIAL PRIMARY KEY,
                   username VARCHAR(50),
                   text VARCHAR(500),
                   followers_count REAL,
                   location VARCHAR(50),
                   sentiment_score REAL); '''

engine.execute(CREATE_QUERY)

s = SentimentIntensityAnalyzer()

# Write functions for each step of the ETL process
def extract():
    '''Extracts tweets from the MongoDB database'''
    tweets = list(tweet_collection.find())[-3:] # The [-2:] ensures that only the last two tweets are extracted
    # tweets is a list of tweets, where each item is a tweet. Each tweet is of the datatype dict or cursor
    return tweets

def transform(tweets):
    '''
    Transform tweets that were extracted from MongoDB

    Parameters:
    -----------
    tweets : List of tweets that were extracted from the MongoDB database.
    '''
    for tweet in tweets:
        tweet['sentiment_score'] = s.polarity_scores(tweet['text'])['compound']
        # This is were the logic will be implemented
        # tweet is a dictionary which is a mutable object
        # when saying tweet['sentiment_score'] = 1, we add a key value pair to the dictionary tweet
        # Eg. tweet is {'username': 'Diana', 'text':'This was a long lecture'}
        # After transforming it it will look like {'username': 'Diana', 'text':'This was a long lecture', 'sentiment_score' = 1}
    return tweets

def load(tweets):
    '''
    Load transformed tweets into the Postgres database

    Parameters:
    -----------
    tweets : List of tweets that were extracted from the MongoDB database and transformed.
    '''
    insert_query = 'INSERT INTO tweets(username, text, followers_count, location, sentiment_score) VALUES (%s, %s, %s, %s, %s)'
    for tweet in tweets:
        engine.execute(insert_query, (tweet['username'], tweet['text'], tweet['followers_count'], tweet['location'], tweet['sentiment_score']))

while True:
    time.sleep(5)
    extracted_tweets = extract()
    transformed_tweets = transform(extracted_tweets)
    load(transformed_tweets)
    logging.warning('---New list of tweets has been written into the Postgres database')
