import logging
import unittest

from parameterized import parameterized

from tests.backtests.backtests import get_recent_trades, run_backtest_for_trade, TradeOutcome
from trader_tweets.service.utilities import init_logging

NUM_TRADES_TO_FETCH = 500

recent_trades = get_recent_trades(num_trades_to_fetch=NUM_TRADES_TO_FETCH)
recent_trades_tuples = [(trade,) for trade in recent_trades]
logging.info('got trades')

class BacktestsRecentTrades(unittest.TestCase):
    @parameterized.expand(recent_trades_tuples)
    def test_recent_tweets(self, trade):
        self._test_trade(trade)

    def _test_trade(self, trade):
        result = run_backtest_for_trade(trade)
        self.assertEqual(TradeOutcome.WIN, result.outcome)
        # self.assertGreaterEqual(result.change_factor, 1.05)


if __name__ == '__main__':
    init_logging()
    unittest.main()
