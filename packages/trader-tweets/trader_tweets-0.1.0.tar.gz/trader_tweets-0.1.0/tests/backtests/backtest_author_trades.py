import unittest

from parameterized import parameterized

from tests.backtests.backtests import get_recent_trades, run_backtest_for_trade, TradeOutcome
from tests.unit.util.cool_test_case import CoolTestCase
from trader_tweets.model.twitter.twitter_traders import PC_PRINCIPLE, TRADER_XO, GANYMEDE
from trader_tweets.service.utilities import init_logging

class BacktestsAuthorTrades(CoolTestCase):

    trader_trades = get_recent_trades(author=GANYMEDE, num_trades_to_fetch=100)
    trade_tuples = [(trade,) for trade in trader_trades]

    total_winnings = 0
    total_losses = 0
    num_wins = 0
    num_losses = 0

    @parameterized.expand(trade_tuples)
    def test_recent_tweets(self, trade):
        self._test_trade(trade)

    def _test_trade(self, trade):
        print('Tweet:', trade.origin_tweet.text)
        result = run_backtest_for_trade(trade)
        self.assertEqual(TradeOutcome.WIN, result.outcome)
        self.assertGreater(result.change_factor, 1.05)
        if result.outcome == TradeOutcome.WIN:
            BacktestsAuthorTrades.total_winnings += result.change_factor
            BacktestsAuthorTrades.num_wins += 1
        elif result.outcome == TradeOutcome.LOSS:
            BacktestsAuthorTrades.total_losses += result.change_factor
            BacktestsAuthorTrades.num_losses += 1

    @classmethod
    def tearDownClass(cls):
        avg_winnings = cls.total_winnings / cls.num_wins
        avg_loss = cls.total_losses / cls.num_losses if cls.num_losses > 0 else 0
        print(f'Average winnings (change factor): {avg_winnings:.2f}')
        print(f'Average loss (change factor): {avg_loss:.2f}')


if __name__ == '__main__':
    init_logging()
    unittest.main()
