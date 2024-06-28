import logging
import os
from typing import List

import requests
from diskcache import Cache

from trader_tweets.model.twitter.simple_tweet import SimpleTweet
from trader_tweets.model.twitter.twitter_user import TwitterUser
from trader_tweets.repository.secret_repository import fetch_secret
from trader_tweets.service.cache_service import CACHE_DIR
from trader_tweets.service.utilities import is_development
from twscrape import API, gather, Tweet

TRADER_TWITTER_LIST_ID = 1526846963945472001

SECRET_NAME_TWITTER_OAUTH_CONSUMER_KEY = 'twitter_api_key'
SECRET_NAME_TWITTER_OAUTH_CONSUMER_SECRET = 'twitter_api_key_secret'
SECRET_NAME_TWITTER_OAUTH_TOKEN = 'twitter_access_token'
SECRET_NAME_TWITTER_OAUTH_TOKEN_SECRET = 'twitter_access_token_secret'

CACHE_TWEETS = os.path.join(CACHE_DIR, 'tweets')
CACHE_AUTHOR_NAMES = os.path.join(CACHE_DIR, 'authors')


async def get_latest_tweets(num_tweets: int) -> List[SimpleTweet]:
    return await fetch_posts_by_list_id_async(TRADER_TWITTER_LIST_ID, num_tweets)


async def fetch_posts_by_list_id_async(list_id: int, post_limit: int) -> List[SimpleTweet]:
    twscrape_db_file_path = os.environ['TWSCRAPE_DB_PATH']
    api = API(twscrape_db_file_path)

    logging.info(f"Fetching posts for {list_id} from Twitter API with limit: {post_limit}")
    posts = await gather(api.list_timeline(list_id, limit=post_limit))
    print(f'Got {len(posts)} from list {list_id}')
    simple_posts = list(map(map_from_twscrape_post_to_simple_tweet, posts))
    return simple_posts


def map_from_twscrape_post_to_simple_tweet(twscrape_post: Tweet) -> SimpleTweet:
    img_url = twscrape_post.media.photos.pop().url \
        if twscrape_post.media is not None and len(twscrape_post.media.photos) > 0 \
        else None

    author = TwitterUser(
        id=twscrape_post.user.id,
        name=twscrape_post.user.displayname,
        username=twscrape_post.user.username,
        profile_image_url=twscrape_post.user.profileImageUrl
    )
    return SimpleTweet(
        id=twscrape_post.id,
        text=twscrape_post.rawContent,
        author=author,
        img_url=img_url,
        timestamp=twscrape_post.date)


def get_author(author_id) -> TwitterUser:
    pass


def get_tweets_by_ids(tweet_ids):
    pass


def clean_tweet_text(text):
    cleaned = text.strip() \
        .replace('\n', ' ') \
        .replace('\r', ' ')

    return cleaned


def get_from_cache(cache, key):
    cache = Cache(cache)
    return cache[key]


def set_in_cache(cache, key, value):
    cache = Cache(cache)
    cache[key] = value


def is_in_cache(cache, key):
    cache = Cache(cache)
    return key in cache


def should_use_cache():
    return is_development()
