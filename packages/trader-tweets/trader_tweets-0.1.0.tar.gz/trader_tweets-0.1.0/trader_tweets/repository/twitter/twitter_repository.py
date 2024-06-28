import logging
import os
from typing import List

from trader_tweets.model.twitter.simple_tweet import SimpleTweet
from trader_tweets.model.twitter.twitter_user import TwitterUser
from trader_tweets.service.cache_service import CACHE_DIR

from trader_tweets.repository.twitter.twscrape_repository import get_latest_tweets as get_latest_tweets_from_twscrape

TRADER_TWITTER_LIST_ID = 1526846963945472001

SECRET_NAME_TWITTER_OAUTH_CONSUMER_KEY = 'twitter_api_key'
SECRET_NAME_TWITTER_OAUTH_CONSUMER_SECRET = 'twitter_api_key_secret'
SECRET_NAME_TWITTER_OAUTH_TOKEN = 'twitter_access_token'
SECRET_NAME_TWITTER_OAUTH_TOKEN_SECRET = 'twitter_access_token_secret'

CACHE_TWEETS = os.path.join(CACHE_DIR, 'tweets')
CACHE_AUTHOR_NAMES = os.path.join(CACHE_DIR, 'authors')


async def get_latest_tweets(num_tweets) -> List[SimpleTweet]:
    return await get_latest_tweets_from_twscrape(num_tweets)


def get_author(author_id) -> TwitterUser:
    pass


def get_tweets_by_ids(tweet_ids):
    pass
