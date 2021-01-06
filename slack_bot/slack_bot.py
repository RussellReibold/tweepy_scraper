import slack
import time
import logging
from sqlalchemy import create_engine

time.sleep(20)

oauth_token = config.oauth_token

client = slack.WebClient(token=oauth_token)

# Connect to the Postgres database
HOST = config.HOSTPOST
USERNAME = config.USERNAME
PORT = config.PORTPOST
DB = config.DB
PASSWORD = config.PASSWORD

engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}', pool_size=50, max_overflow=100)

SELECT_TWEET = ''' SELECT text FROM tweets ORDER BY id DESC LIMIT 1; '''

tweet = engine.execute(SELECT_TWEET).first()

client.chat_postMessage(channel='#random', text=f"Here is a Bitcoin Tweet: {tweet}")

while True:
    time.sleep(120)
    tweet = engine.execute(SELECT_TWEET).first()
    client.chat_postMessage(channel='#random', text=f"Here is a Bitcoin: {tweet}")
    logging.warning('--New Tweet was posted to Slack')
'''

Things to work on this python file.

1. If we want to post to slack continously we need to write a loop
while True:
    ...
2. Post actual tweets from the Postgres database
- Connect to Postgres (sqlalchemy, psycopg2-binary)
- Write a query that extracts a tweet and its sentiment polarity_scores

'''
