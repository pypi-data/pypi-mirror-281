import unittest
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Tuple, Optional

from parameterized import parameterized

from trader_tweets.model.classified_tweet import ClassifiedTweet
from trader_tweets.model.trade import Trade, Direction
from trader_tweets.model.tweet_type import TweetType
from trader_tweets.model.twitter.twitter_user import TwitterUser
from trader_tweets.tweet_parsing import find_opening_trade_in_tweet

default_date = datetime.now()

@dataclass
class TweetSymbols:
    tweet: str
    expected_symbols: List[str]

def get_new_tweet(tweet_text: str) -> ClassifiedTweet:
    return ClassifiedTweet(
        text=tweet_text,
        classification=TweetType.TRADE,
        timestamp=default_date,
        author=TwitterUser(id=123, name='test', username='test'),
        id=123,
        img_url=None
    )


TRADEABLE_TWEETS: List[Tuple[str, Trade]] = [
    # now the correct type
    (
        'bought MINA at 22.4',
        Trade( symbol='MINAUSD', direction=Direction.LONG, date=default_date )
    ),
    (
        'long $DOGE at 0.25. Looking for a move to 0.3',
        Trade( symbol='DOGEUSD', direction=Direction.LONG, date=default_date )
    ),
    (
        'i\'m short LTCUSD at 38, stop at 40, target 35',
        Trade( symbol='LTCUSD', direction=Direction.SHORT, date=default_date )
    ),
    (
        '$MATIC Ive got short positioning running from 1.34 I added more this morning at 1.25\'s First time this year I\'ve opted to look for a swing short on Matic Poly Gone. https://t.co/F3XxL8ZiG6',
        Trade( symbol='MATICUSD', direction=Direction.SHORT, date=default_date )
    ),
    (
        'Thoughts: - Weekend freedom from SPX correlation begins. - 24 hours of fud and no new lows. - A handful of alts holding key levels. Grabbed some alts for a bounce, buying strength, and $LOOKS is one. https://t.co/BjVF4J5oMJ',
        Trade( symbol='LOOKSUSD', direction=Direction.LONG, date=default_date )
     ),
    (
        'tomorrow is a big day for $BTCUSD',
        Trade( symbol='BTCUSD', direction=Direction.LONG, date=default_date )
    ),
    (
        'expecting to see a great week for X2Y2',
        Trade( symbol='X2Y2USD', direction=Direction.LONG, date=default_date )
    ),
    (
        'tping from AUDIO',
        Trade( symbol='AUDIOUSD', direction=Direction.SHORT, date=default_date )
     ),
    (
        'sl hit on JASMY',
        Trade( symbol='JASMYUSD', direction=Direction.SHORT, date=default_date )
    ),
]


NON_TRADEABLE_TWEETS: List[str] = [
    'abc',
    'a b c d e f g h i j k l m n o p q r s t u v w x y z',
    'Ive got short positioning running from 1.34 I added more this morning at 1.25s First time this year Ive opted to look for a swing short on Matic Poly Gone. https://t.co/F3XxL8ZiG6',
    'aslong as we stay below yellow box, i expect it to go lower https://t.co/nHxa6uwb2S',
    'unless it reclaims trendline...i wouldnt get too excited about longs just yet https://t.co/7ruIdiryQH',
    'we moving https://t.co/731idYg8vN https://t.co/yc1OHXEiPC',
    'DXY is indeed bouncing https://t.co/KOLYhANCkn',
    '$ETHUSD - unless it reclaims trendline...i wouldnt get too excited about longs just yet https://t.co/7ruIdiryQH',
]


class TestTweetParsing(unittest.TestCase):
    @parameterized.expand(TRADEABLE_TWEETS)
    def test_tradeable_tweets_correctly_map_to_trade(self, tweet_text, expected_trade):
        tweet: ClassifiedTweet = get_new_tweet(tweet_text)
        trade = find_opening_trade_in_tweet(tweet)
        self.assertEqual(expected_trade, trade)

    @parameterized.expand(NON_TRADEABLE_TWEETS)
    def test_non_tradeable_tweets_are_correctly_identified(self, tweet_text):
        tweet: ClassifiedTweet = get_new_tweet(tweet_text)
        trade = find_opening_trade_in_tweet(tweet)
        self.assertIsNone(trade)


if __name__ == '__main__':
    unittest.main()
