import unittest
from typing import List, Tuple

from parameterized import parameterized

from trader_tweets.mapper.binance import cleanse_binance_klines

binance_klines_examples: List[Tuple[List[List], List[List]]] = [
    (
        [[1675551600000, '0.1', '0.2', '0.3', '0.4', 4000]],
        [['2023-02-04T23:00:00+00:00', 0.1, 0.2, 0.3, 0.4, 4000]]
    )
]

class TestBinanceMapper(unittest.TestCase):
    @parameterized.expand(binance_klines_examples)
    def test_trade_tweet(self, binance_klines, expected_clean_klines):
        self.assertEqual(expected_clean_klines, cleanse_binance_klines(binance_klines))

