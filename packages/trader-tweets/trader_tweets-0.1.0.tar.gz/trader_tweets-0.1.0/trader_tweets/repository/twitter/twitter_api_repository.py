import logging
import os
from typing import List

import requests
from requests_oauthlib import OAuth1
from diskcache import Cache

from trader_tweets.model.twitter.simple_tweet import SimpleTweet
from trader_tweets.model.twitter.twitter_user import TwitterUser
from trader_tweets.repository.secret_repository import fetch_secret
from trader_tweets.service.cache_service import CACHE_DIR
from trader_tweets.service.utilities import is_development

TRADER_TWITTER_LIST_ID = 1526846963945472001

SECRET_NAME_TWITTER_OAUTH_CONSUMER_KEY = 'twitter_api_key'
SECRET_NAME_TWITTER_OAUTH_CONSUMER_SECRET = 'twitter_api_key_secret'
SECRET_NAME_TWITTER_OAUTH_TOKEN = 'twitter_access_token'
SECRET_NAME_TWITTER_OAUTH_TOKEN_SECRET = 'twitter_access_token_secret'

CACHE_TWEETS = os.path.join(CACHE_DIR, 'tweets')
CACHE_AUTHOR_NAMES = os.path.join(CACHE_DIR, 'authors')


def get_latest_tweets(num_tweets) -> List[SimpleTweet]:
    params = {
        'max_results': num_tweets,
        'tweet.fields': 'id,text,author_id,created_at,entities',
        'expansions': 'attachments.media_keys',
        'media.fields': 'type,url'
    }

    response = fetch_from_twitter_api('2/lists/{}/tweets'.format(TRADER_TWITTER_LIST_ID), params)
    logging.info(f'twitter response: {response}')
    simple_tweets = map_api_tweets_to_simplified_tweets(response['data'])

    return simple_tweets


def generate_auth():
    return OAuth1(
        fetch_secret(SECRET_NAME_TWITTER_OAUTH_CONSUMER_KEY, '3'),
        fetch_secret(SECRET_NAME_TWITTER_OAUTH_CONSUMER_SECRET, '3'),
        fetch_secret(SECRET_NAME_TWITTER_OAUTH_TOKEN, '3'),
        fetch_secret(SECRET_NAME_TWITTER_OAUTH_TOKEN_SECRET, '4')
    )


def fetch_from_twitter_api(path, params=None):
    if params is None:
        params = {}
    url = 'https://api.twitter.com/' + path
    auth = generate_auth()

    try:
        response = requests.get(url, params=params, auth=auth)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error('Error getting tweets: ' + str(response.status_code) + ' ' + response.text)
            return None
    except Exception as e:
        logging.error('Error getting tweets: ' + str(e))
        return None


def get_author(author_id) -> TwitterUser:
    if should_use_cache() and is_in_cache(CACHE_AUTHOR_NAMES, author_id):
        return get_from_cache(CACHE_AUTHOR_NAMES, author_id)

    response = fetch_from_twitter_api('2/users/{id}'.format(id=author_id), {'user.fields': 'name,profile_image_url'})
    data = response['data']
    user = TwitterUser(id=author_id, name=data['name'], username=data['username'], profile_image_url=data['profile_image_url'])

    if should_use_cache():
        set_in_cache(CACHE_AUTHOR_NAMES, author_id, user)
    return user


def get_tweets_by_ids(tweet_ids):
    ids_list_to_string = ','.join(map(str, tweet_ids))
    if should_use_cache() and is_in_cache(CACHE_TWEETS, ids_list_to_string):
        return get_from_cache(CACHE_TWEETS, ids_list_to_string)

    tweets = get_tweets_from_twitter_api(ids_list_to_string)
    simple_tweets = map_api_tweets_to_simplified_tweets(tweets)

    if should_use_cache():
        set_in_cache(CACHE_TWEETS, ids_list_to_string, simple_tweets)

    return simple_tweets


def get_tweets_from_twitter_api(tweet_ids_str):
    response = fetch_from_twitter_api('2/tweets', {
        'ids': tweet_ids_str,
        'tweet.fields': 'id,text,author_id',
        'expansions': 'attachments.media_keys',
        'media.fields': 'type,url'
    })
    return response['data']


def map_api_tweets_to_simplified_tweets(tweets):
    simplified: List[SimpleTweet] = []
    for tweet in tweets:
        logging.debug('Tweet from API: ', tweet)
        tweet_text = tweet['text']
        cleaned_tweet_text = clean_tweet_text(tweet_text)
        author = get_author(tweet['author_id'])
        img_url = tweet['includes']['media'][0]['url'] \
            if 'includes' in tweet and 'media' in tweet['includes'] \
            else None
        timestamp = tweet['created_at'] if 'created_at' in tweet else None

        simplified.append(
            SimpleTweet(
                id=int(tweet['id']),
                text=cleaned_tweet_text,
                author=author,
                img_url=img_url,
                timestamp=timestamp
            )
        )

    return simplified


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
