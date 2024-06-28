import unittest
from datetime import datetime
from typing import List, Tuple

from parameterized import parameterized

from tests.backtest import run_backtest_for_trade, TradeOutcome
from trader_tweets.model.trade import Trade, Direction

winning_trades: List[Tuple[Trade, TradeOutcome]] = [
    (Trade(symbol='BTCUSDT', direction=Direction.LONG, date=datetime(2023, 1, 6, 23, 0, 0, 0)), TradeOutcome.WIN),
    (Trade(symbol='BTCUSDT', direction=Direction.SHORT, date=datetime(2023, 2, 18, 23, 0, 0, 0)), TradeOutcome.WIN),
    (Trade(symbol='BTCUSDT', direction=Direction.LONG, date=datetime(2021, 9, 21, 23, 0, 0, 0)), TradeOutcome.WIN),
    (Trade(symbol='BTCUSDT', direction=Direction.LONG, date=datetime(2019, 6, 12, 23, 0, 0, 0)), TradeOutcome.WIN),
    (Trade(symbol='SOLUSDT', direction=Direction.LONG, date=datetime(2023, 1, 3, 23, 0, 0, 0)), TradeOutcome.WIN),
    (Trade(symbol='SOLUSDT', direction=Direction.SHORT, date=datetime(2023, 2, 6, 23, 0, 0, 0)), TradeOutcome.WIN),
    (Trade(symbol='APTUSDT', direction=Direction.LONG, date=datetime(2023, 1, 8, 23, 0, 0, 0)), TradeOutcome.WIN),
    # losing trades
    (Trade(symbol='BTCUSDT', direction=Direction.SHORT, date=datetime(2023, 1, 6, 23, 0, 0, 0)), TradeOutcome.LOSS),
    (Trade(symbol='BTCUSDT', direction=Direction.LONG, date=datetime(2023, 2, 18, 23, 0, 0, 0)), TradeOutcome.LOSS),
    (Trade(symbol='BTCUSDT', direction=Direction.SHORT, date=datetime(2021, 9, 21, 23, 0, 0, 0)), TradeOutcome.LOSS),
    (Trade(symbol='BTCUSDT', direction=Direction.SHORT, date=datetime(2019, 6, 12, 23, 0, 0, 0)), TradeOutcome.LOSS),
    (Trade(symbol='SOLUSDT', direction=Direction.SHORT, date=datetime(2023, 1, 3, 23, 0, 0, 0)), TradeOutcome.LOSS),
    (Trade(symbol='SOLUSDT', direction=Direction.LONG, date=datetime(2023, 2, 6, 23, 0, 0, 0)), TradeOutcome.LOSS),
    (Trade(symbol='APTUSDT', direction=Direction.SHORT, date=datetime(2023, 1, 8, 23, 0, 0, 0)), TradeOutcome.LOSS),
    (Trade(symbol='WAVESUSDT', direction=Direction.SHORT, date=datetime(2022, 5, 29, 23, 0, 0, 0)), TradeOutcome.LOSS)
]

class BacktestCuratedTrades(unittest.TestCase):

    @parameterized.expand(winning_trades)
    def test_curated_trades(self, winning_trade, expected_outcome):
        result = run_backtest_for_trade(winning_trade)
        self.assertEqual(expected_outcome, result)
