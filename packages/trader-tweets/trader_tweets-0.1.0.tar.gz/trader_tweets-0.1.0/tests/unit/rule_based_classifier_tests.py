# test rule_based_classifier with unittest and parameterized test cases

import unittest
from parameterized import parameterized

from trader_tweets.model.twitter.simple_tweet import SimpleTweet
from trader_tweets.model.twitter.twitter_user import TwitterUser
from trader_tweets.service.classifier.tweet_type.classifier import classify_tweet
from trader_tweets.trade_tweet_job import TweetType

trade_tweet_examples = [
    # "Bidding 1400",  # keyword: bidding
    # "Selling 2800",  # keyword: selling
    # "Will bid at around 1400",  # keyword: bid
    # "Will sell at around 2800",  # keyword: sell
    "Got stopped at 2950",  # keyword: stopped
]

prediction_tweet_examples = [
    "Prediction: I think the btc gets as high as 100k this year",  # keyword: prediction
]

not_interesting_tweet_examples = [
    "I am a bot",  # keyword: bot
    "lol Barry Silbert",  # keyword: lol
    "haha @ThinkingBitmex",  # keyword: hah
    "wtf @ThinkingBitmex",  # keyword: wtf
    "um this too weird",  # keyword: um
    "uh pizza",  # keyword: uh
    "69 caller",  # keyword: 69
    "this rip is such a meme",  # keyword: meme
    "$COCK will moon",  # keyword: moon
    "this is from bitboy",  # keyword: bitboy
    "the rainbow formula is working!",  # keyword: rainbow
    "RT: check dis out"  # retweet
    "https://t.co/42ag4HESTy",  # just a link
    "🤝 https://t.co/42ag4HESTy"  # a link with not much else
]


class TestRuleBasedClassifier(unittest.TestCase):
    @parameterized.expand(trade_tweet_examples)
    def test_trade_tweet(self, tweet_text):
        self._test_tweet_is_correct_type(tweet_text, TweetType.TRADE)

    @parameterized.expand(prediction_tweet_examples)
    def test_prediction_tweet(self, tweet_text):
        self._test_tweet_is_correct_type(tweet_text, TweetType.PREDICTION)

    @parameterized.expand(not_interesting_tweet_examples)
    def test_not_interesting_tweet(self, tweet_text):
        self._test_tweet_is_correct_type(tweet_text, TweetType.NOT_INTERESTING)

    def _test_tweet_is_correct_type(self, tweet_text: str, expected_tweet_type: TweetType):
        user = TwitterUser(id=123, username="test", name="test")
        tweet = SimpleTweet(id=123, text=tweet_text, author=user,
                            img_url="https://pbs.twimg.com/media/EqZ0Z5hXMAA8Z5j?format=jpg&name=small")
        classified_tweet = classify_tweet(tweet)
        self.assertEqual(classified_tweet.classification, expected_tweet_type)


if __name__ == '__main__':
    unittest.main()
