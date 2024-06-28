import unittest
from dataclasses import dataclass
from typing import List, Dict, Tuple

from parameterized import parameterized
from trader_tweets.tweet_parsing import parse_symbols_from_tweet


@dataclass
class TweetSymbols:
    tweet: str
    expected_symbols: List[str]


TWEETS_WITH_SYMBOLS: List[Tuple[str, List[str]]] = [
    # now the correct type
    ('BTC', ['BTCUSD']),
    ('$btc', ['BTCUSD']),
    ('$BTC', ['BTCUSD']),
    ('BTC.', ['BTCUSD']),
    ('BTC,', ['BTCUSD']),
    ('BTC?', ['BTCUSD']),
    ('BTCUSD.', ['BTCUSD']),
    ('BTCUSD', ['BTCUSD']),
    ('$BTCUSD', ['BTCUSD']),
    ('BTCUSDT', ['BTCUSDT']),
    ('ETHBTC', ['ETHBTC']),
    ('ETHUSD', ['ETHUSD']),
    ('SOL', ['SOLUSD']),
    ('SOLUSD', ['SOLUSD']),
    ('$MATIC Ive got short positioning running from 1.34 I added more this morning at 1.25\'s First time this year I\'ve opted to look for a swing short on Matic Poly Gone. https://t.co/F3XxL8ZiG6', ['MATICUSD']),
    ('$ETHBTC - aslong as we stay below yellow box, i expect it to go lower https://t.co/nHxa6uwb2S', ['ETHBTC']),
    ('$ETHUSD - unless it reclaims trendline...i wouldnt get too excited about longs just yet https://t.co/7ruIdiryQH', ['ETHUSD']),
    ('$SHIB - we moving https://t.co/731idYg8vN https://t.co/yc1OHXEiPC', ['SHIBUSD']),
    ('DXY is indeed bouncing https://t.co/KOLYhANCkn', ['DXY']),
    ('High Level Thoughts - BTC &amp; ETH still ranging, failure to breakdown following FTX collapse is encouraging for bulls - gives room for alts w/ out bagholders (new launches) and coins w/ strong narratives as good trades', ['BTCUSD', 'ETHUSD']),
    ('ETH - ETHBTC has been much stronger than last bear market so far - ETH has been deflationary at times since upgrade to PoS, should have tangible effects on how it trades once activity picks back up again https://t.co/SvFwFU', ['ETHUSD', 'ETHBTC']),
    ('Thoughts: - Weekend freedom from SPX correlation begins. - 24 hours of fud and no new lows. - A handful of alts holding key levels. Grabbed some alts for a bounce, buying strength, and $LOOKS is one. https://t.co/BjVF4J5oMJ', ['SPX', 'LOOKSUSD']),
    ('BTCUSD - unless it reclaims trendline...i wouldnt get too excited about longs just yet https://t.co/7ruIdiryQH', ['BTCUSD']),
    ('tomorrow is a big day for $BTCUSD', ['BTCUSD']),
    ('expecting to see a great week X2Y2', ['X2Y2USD']),
    ('tping from AUDIO', ['AUDIOUSD']),
    ('sl hit on JASMY', ['JASMYUSD']),
    # ('Ive got short positioning running from 1.34 I added more this morning at 1.25s First time this year Ive opted to look for a swing short on Matic Poly Gone. https://t.co/F3XxL8ZiG6', ['MATICUSD'] ),
]

TWEETS_WITHOUT_SYMBOLS = [
    'abc',
    'a b c d e f g h i j k l m n o p q r s t u v w x y z',
    'Ive got short positioning running from 1.34 I added more this morning at 1.25s First time this year Ive opted to look for a swing short on Matic Poly Gone. https://t.co/F3XxL8ZiG6',
    'aslong as we stay below yellow box, i expect it to go lower https://t.co/nHxa6uwb2S',
    'unless it reclaims trendline...i wouldnt get too excited about longs just yet https://t.co/7ruIdiryQH',
    'we moving https://t.co/731idYg8vN https://t.co/yc1OHXEiPC',
    'this is indeed bouncing https://t.co/KOLYhANCkn',
    'EURJPY',
    'HODL bitcoin'
    'GG from SEC is not a good sign for crypto',
]


class TestTweetParsing(unittest.TestCase):
    @parameterized.expand(TWEETS_WITH_SYMBOLS)
    def test_tweets_with_symbols_are_detected(self, tweet_text, expected_symbols):
        symbols = parse_symbols_from_tweet(tweet_text)
        self.assertGreater(len(symbols), 0)

    @parameterized.expand(TWEETS_WITHOUT_SYMBOLS)
    def test_tweets_without_symbols_are_not_detected(self, tweet_text):
        self.assertEqual(0, len(parse_symbols_from_tweet(tweet_text)))

    @parameterized.expand(TWEETS_WITH_SYMBOLS)
    def test_tweets_with_symbols_are_parsed_correctly(self, tweet_text, expected_symbols):
        # assert if all elements in expected_symbols are in the list returned by parse_symbols_from_tweet
        # self.assertTrue(all(symbol in parse_symbols_from_tweet(tweet_text) for symbol in expected_symbols))
        symbols = parse_symbols_from_tweet(tweet_text)
        self.assertEqual(expected_symbols, symbols)


if __name__ == '__main__':
    unittest.main()
