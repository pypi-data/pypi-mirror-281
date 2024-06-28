# periodical task to:
# 1) get the latest tweets from traders
# 2) analyze the tweets to determine if they are trades
# 3) update the database with the trades
# 4) interesting tweets: post to discord

import logging
import os
from typing import List

from trader_tweets.model.tweet_type import TweetType
from trader_tweets.service.classifier.tweet_type.classifier import classify_tweets
from trader_tweets.model.classified_tweet import ClassifiedTweet
from trader_tweets.model.twitter.simple_tweet import SimpleTweet
from trader_tweets.repository.classified_tweets_repository import ClassifiedTweetsRepository
from trader_tweets.repository.twitter.twitter_repository import get_latest_tweets
from trader_tweets.service.discord_service import post_classified_tweet_to_discord, DISCORD_WEBHOOK_URL_CHANNEL_ALPHA, \
    DISCORD_WEBHOOK_URL_CHANNEL_ALL

NUM_TWEETS_TO_ANALYSE = os.environ['NUM_TWEETS_TO_ANALYSE']

classified_tweet_repo = ClassifiedTweetsRepository()


def post_classifications_to_data_store(classified_tweets: List[ClassifiedTweet]):
    logging.info('posting classified tweets to firestore & discord')

    # add to firestore database
    classified_tweet_repo.set_classified_tweets(classified_tweets)

    # post the new tweets to discord too (regardless of classification)
    for tweet in classified_tweets:
        post_classified_tweet_to_discord(tweet, DISCORD_WEBHOOK_URL_CHANNEL_ALL)


async def run_trader_tweet_job():
    logging.info('Starting trader tweet job')

    tweets = await get_latest_tweets(int(NUM_TWEETS_TO_ANALYSE))
    new_tweets = filter_out_already_classified(tweets)
    logging.info('Analyzing ' + str(len(new_tweets)) + ' new tweets:')
    logging.info([tweet.text for tweet in new_tweets])

    classified = classify_tweets(new_tweets)
    post_classifications_to_data_store(classified)
    interesting_tweets = filter_out_boring_tweets(classified)

    if len(interesting_tweets) == 0:
        logging.info('No new interesting tweets found')
        return

    logging.info('New interesting tweets: ' + str(len(interesting_tweets)))
    for tweet in interesting_tweets:
        logging.info("{author}: {text} ({clazz})"
                     .format(author=tweet.author.name, text=tweet.text, clazz=tweet.classification))
        post_classified_tweet_to_discord(tweet, DISCORD_WEBHOOK_URL_CHANNEL_ALPHA)


def filter_out_already_classified(tweets: List[SimpleTweet]) -> List[SimpleTweet]:
    return [tweet for tweet in tweets if not classified_tweet_repo.is_tweet_classified(tweet.id)]


def filter_out_boring_tweets(classifications: List[ClassifiedTweet]) -> List[ClassifiedTweet]:
    interesting_tweets = []
    for tweet_classified in classifications:
        if tweet_classified.classification == TweetType.TRADE \
                or tweet_classified.classification == TweetType.PREDICTION:
            interesting_tweets.append(tweet_classified)

    return interesting_tweets
