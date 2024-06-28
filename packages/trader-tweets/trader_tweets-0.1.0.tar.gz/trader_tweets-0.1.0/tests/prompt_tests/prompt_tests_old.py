import unittest
from parameterized import parameterized

from main import init_logging
from trader_tweets.repository.twitter.twitter_repository import get_tweets_by_ids
from trader_tweets.service.classifier.tweet_type.classifier import classify_tweet
from trader_tweets.trade_tweet_job import TweetType

reference_tweets = {
    TweetType.TRADE: [
        1544810050040086529,
        1544677604510367744,
        1544328416937316353,
        1544322605942980610,
        1523127881425371137,
        1544690863690973184,
        1544748019962216459,
        1544671614972878848
    ],
    TweetType.PREDICTION: [
        1519761964964233218,
        # 1544833154665660416,  # kinda a joke
        1544865122639921152,
        1544767786186117121,
        1528778813328478211,
        1528778892189868033,
        1523462305144397826,
        1519872655037509632,
        1544999828102553600,
        1544999828102553600
    ],
    TweetType.NOT_INTERESTING: [
        1544959430944382976,
        1544971607327838210,
        1544832488790450177,
        1544000741504860161,
        1544000963786203136,
        1544002105689636864,
        1543718633658060802,
        1536727156549722114,
        1547130341093249025,
        1547125497670160384,
        1547125326433714176
    ],
}

parameterized_test_cases_trade = map(
    lambda tweet_id: (tweet_id, TweetType.TRADE), reference_tweets[TweetType.TRADE]
)
parameterized_test_cases_prediction = map(
    lambda tweet_id: (tweet_id, TweetType.PREDICTION), reference_tweets[TweetType.PREDICTION]
)
parameterized_test_cases_not_interesting = map(
    lambda tweet_id: (tweet_id, TweetType.NOT_INTERESTING), reference_tweets[TweetType.NOT_INTERESTING]
)

parameterized_test_cases = {
    TweetType.TRADE: parameterized_test_cases_trade,
    TweetType.PREDICTION: parameterized_test_cases_prediction,
    TweetType.NOT_INTERESTING: parameterized_test_cases_not_interesting
}


class PromptTestsOld(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tweets = {
            TweetType.TRADE: get_tweets_by_ids(reference_tweets[TweetType.TRADE]),
            TweetType.PREDICTION: get_tweets_by_ids(reference_tweets[TweetType.PREDICTION]),
            TweetType.NOT_INTERESTING: get_tweets_by_ids(reference_tweets[TweetType.NOT_INTERESTING])
        }

    @parameterized.expand(parameterized_test_cases[TweetType.TRADE])
    def test_trade_tweets(self, tweet_id, expected_tweet_type):
        self.check_tweet_type(tweet_id, expected_tweet_type)

    @parameterized.expand(parameterized_test_cases[TweetType.PREDICTION])
    def test_prediction_tweets(self, tweet_id, expected_tweet_type):
        self.check_tweet_type(tweet_id, expected_tweet_type)

    @parameterized.expand(parameterized_test_cases[TweetType.NOT_INTERESTING])
    def test_not_interesting_tweets(self, tweet_id, expected_tweet_type):
        self.check_tweet_type(tweet_id, expected_tweet_type)

    def check_tweet_type(self, tweet_id, expected_tweet_type):
        expected_tweets = self.tweets[expected_tweet_type]
        tweet = next((tweet for tweet in expected_tweets if tweet.id == tweet_id), None)
        if tweet is None:
            raise Exception(f"Tweet with id {tweet_id} not found in expected tweets")
        classification = classify_tweet(tweet).classification
        self.assertEqual(expected_tweet_type, classification)

    def get_parameterized_test_cases(self, expected_tweet_type):
        # switch case in python
        return parameterized_test_cases[expected_tweet_type]


if __name__ == '__main__':
    init_logging()
    unittest.main()
