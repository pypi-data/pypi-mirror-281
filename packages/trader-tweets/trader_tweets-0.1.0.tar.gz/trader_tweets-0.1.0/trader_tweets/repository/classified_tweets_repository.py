# this class fetches and writes to the trader tweets database
# the is accessed by connecting to a google firestore database
import logging
import os
from typing import List

from google.cloud import firestore

from trader_tweets.model.classified_tweet import ClassifiedTweet
from trader_tweets.model.tweet_type import TweetType
from trader_tweets.repository.mapper.classified_tweet_mapper import map_firestore_tweets_to_trader_tweets, \
    map_tweet_obj_to_db_record
from trader_tweets.service.cache_service import should_use_cache, set_in_cache, get_from_cache

TRADER_TWEET_CLASSIFICATION_COLLECTION = 'trader-tweets'

class ClassifiedTweetsRepository:
    gcp_project_id = os.environ['GCP_PROJECT_ID']

    def __init__(self):
        self.db = None

    def _initialise_db_connection(self):
        db = firestore.Client(project=self.gcp_project_id)
        return db

    def _get_db(self):
        if self.db is None:
            self.db = self._initialise_db_connection()

        return self.db

    def set_classified_tweets(self, classified_tweets):
        if len(classified_tweets) == 0:
            return

        logging.info('Setting {} classified tweets to database'.format(len(classified_tweets)))
        for tweet in classified_tweets:
            self.set_classified_tweet(tweet)

    def set_classified_tweet(self, classified_tweet):
        db_tweet = map_tweet_obj_to_db_record(classified_tweet)

        db = self._get_db()
        db_collection = db.collection(TRADER_TWEET_CLASSIFICATION_COLLECTION)
        document = db_collection.document(str(db_tweet.tweet_id))
        document.set(db_tweet.__dict__)

    def is_tweet_classified(self, tweet_id):
        db = self._get_db()
        db_collection = db.collection(TRADER_TWEET_CLASSIFICATION_COLLECTION)
        document = db_collection.document(str(tweet_id))
        return document.get().exists

    def fetch_tweet_classifications(self):
        db = self._get_db()
        db_collection = db.collection(TRADER_TWEET_CLASSIFICATION_COLLECTION)
        db_tweets = db_collection.stream()
        return db_tweets

    def fetch_latest_tweets(self, type_filter: TweetType = None, author: str = None, offset: int = 0, limit: int = 10) -> List[ClassifiedTweet]:
        # first check if in cache, to save on gcp costs
        if should_use_cache():
            cache_key = 'latest_tweets_{}_{}_{}_{}'.format(type_filter.name if type_filter else None,
                                                           author, offset, limit)
            value = get_from_cache(cache_key)
            if value is not None:
                return set_in_cache(cache_key, value)

        # else get from db
        db = self._get_db()
        db_collection = db.collection(TRADER_TWEET_CLASSIFICATION_COLLECTION)
        query = db_collection \
            .offset(offset) \
            .order_by('timestamp', direction=firestore.Query.DESCENDING)

        if type_filter is not None:
            query = query.where('type', '==', type_filter.name)

        if author is not None:
            query = query.where('author', '==', author)

        db_tweets = query \
            .limit(limit) \
            .stream()

        return map_firestore_tweets_to_trader_tweets(db_tweets)


    def fetch_tweets_with_manual_label(self, limit: int) -> List[ClassifiedTweet]:
        db = self._get_db()
        db_collection = db.collection(TRADER_TWEET_CLASSIFICATION_COLLECTION)
        db_tweets = db_collection \
            .where('manual_label', '!=', "") \
            .limit(limit) \
            .stream()

        return map_firestore_tweets_to_trader_tweets(db_tweets)