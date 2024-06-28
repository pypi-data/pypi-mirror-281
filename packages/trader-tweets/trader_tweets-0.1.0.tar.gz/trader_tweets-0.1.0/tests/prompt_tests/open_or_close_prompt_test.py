import unittest

from parameterized import parameterized

from trader_tweets.tweet_parsing import OpeningClosing, is_opening_or_closing_trade

OPENING_TRADES = [
    "$BTC   First time I'm *swing* shorting btc this year.  Covered on stream multiple times where I've wanted to be a seller.  Entry 25.2 https://t.co/e3MdMRhSEC https://t.co/lwcQytHGOC https://t.co/54uRI4HpOd",
    "Shorted $FTM 54 and 58 cents   2/3rd will cut if acceptance above 60 cents and wait if btc pushes to 24.5 25.5 (level I’ve been wanting to trade)  Won’t always be right but I’ll always be patient and put my balls on the line. https://t.co/TlIRalQYF4",
    "$MATIC Ive got short positioning running from 1.34 I added more this morning at 1.25's  First time this year I've opted to look for a swing short on Matic Poly Gone. https://t.co/F3XxL8ZiG6",
    "$OP Got some lovely fills overnight  Not ruling out a push higher if btc goes up... https://t.co/qYVnE1O2t4",
    "$GBPUSD Third time shorting 1.24's  Previous 2 wins were from 1.24 &gt; 1.23  Third time fortunate?",
]

CLOSING_TRADES = [
    "$OP Done ✅  Ran local highs - over / under - below mid - trigger  Range low - profit  Onto the next one... https://t.co/ltjbXUAxwo",
    "$SOL - Trade I took live on Mondays stream ✅  2.5R banked. https://t.co/kcg33QLUQD",
    "All shorts closed 🤝 Livestream Sunday at 7pm UTC Will focus on alt setups for the week ahead - posting link tomorrow. https://t.co/QvtA9mOamh",
    "$BTC Trade done ✅  Level range trade closed.  Swing position still running. https://t.co/eQslootORq",
    "$AUDUSD ... tightened stops - scaled off 1/3 https://t.co/RepCacFDdj https://t.co/y7kQmFYHCm", # semi-close
    "$EUR cut entry for a scratch in hope of better positioning higher with dollar pushing lower.  Also wanting GBP to trade 1.245s maybe 1.25 at a push then look for trigger on way down https://t.co/iSi5TqknJ6 https://t.co/645qLgc0hi",
]

class OpenClosePromptTests(unittest.TestCase):

    @parameterized.expand(OPENING_TRADES)
    def test_opening_tweets(self, opening_tweet):
        result = is_opening_or_closing_trade(opening_tweet)
        self.assertEqual(OpeningClosing.OPENING, result)


    @parameterized.expand(CLOSING_TRADES)
    def test_closing_tweets(self, opening_tweet):
        result = is_opening_or_closing_trade(opening_tweet)
        self.assertEqual(OpeningClosing.CLOSING, result)
