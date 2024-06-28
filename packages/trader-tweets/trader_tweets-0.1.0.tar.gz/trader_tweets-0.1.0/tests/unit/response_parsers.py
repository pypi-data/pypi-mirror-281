import unittest
from typing import List, Tuple

from parameterized import parameterized

from trader_tweets.model.prompt.bullish_bearish import BuyingSelling
from trader_tweets.strategy.response_parsers import parse_buying_or_selling_response

GPT_RESPONSES: List[Tuple[str, BuyingSelling]] = [
    # buying
    ('buy', BuyingSelling.BUYING),
    ('buying', BuyingSelling.BUYING),
    ('buying. The user is', BuyingSelling.BUYING),
    ('a buy signal. The', BuyingSelling.BUYING),

    # selling
    ('sell', BuyingSelling.SELLING),
    ('selling', BuyingSelling.SELLING),
    ('selling. The user is', BuyingSelling.SELLING),
    ('about selling. The author', BuyingSelling.SELLING),
    ('a sell signal', BuyingSelling.SELLING)
]

class ResponseParser(unittest.TestCase):
    @parameterized.expand(GPT_RESPONSES)
    def test_parse_buying_or_selling_response(self, response_text, expected_buying_selling):
        result = parse_buying_or_selling_response(response_text)
        self.assertEqual(expected_buying_selling, result)


if __name__ == '__main__':
    unittest.main()
