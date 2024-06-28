import logging
from datetime import datetime
from enum import Enum
import backtrader as bt

import pandas as pd

from trader_tweets.service.binance_service import filter_out_trades_with_symbols_not_on_binance
from trader_tweets.repository.binance_repository import get_price_data_from_date
from trader_tweets.strategy.trade.simple_symmetric import SimpleSymmetricStrategy
from trader_tweets.mapper.binance import cleanse_binance_klines
from trader_tweets.model.trade import Trade, Direction
from trader_tweets.model.tweet_type import TweetType
from trader_tweets.repository.classified_tweets_repository import ClassifiedTweetsRepository
from trader_tweets.service.utilities import init_logging
from trader_tweets.tweet_parsing import find_opening_trade_in_tweet, is_tweet_tradeable

DEFAULT_NUM_TWEETS_TO_FETCH = 20


class TradeOutcome(Enum):
    WIN = 1
    LOSS = 2
    CANCELLED = 3

class TradeResult:
    outcome: TradeOutcome
    change_factor: float

    def __init__(self, outcome: TradeOutcome, change_factor: float):
        self.outcome = outcome
        self.change_factor = change_factor

def get_recent_trades(author: str = None, num_trades_to_fetch: int = DEFAULT_NUM_TWEETS_TO_FETCH) -> list[Trade]:
    repo = ClassifiedTweetsRepository()
    recent_trade_tweets = repo.fetch_latest_tweets(
        type_filter=TweetType.TRADE,
        author=author,
        limit=num_trades_to_fetch)

    trades = [find_opening_trade_in_tweet(trade_tweet) for trade_tweet in recent_trade_tweets
              if is_tweet_tradeable(trade_tweet)]
    trades_not_none = list(filter(lambda trade: trade is not None, trades))
    trades_for_binance = filter_out_trades_with_symbols_not_on_binance(trades_not_none)

    logging.info(f'num trades: {len(trades)}')
    logging.info(f'tradeable on binance: {len(trades_for_binance)}')
    logging.info('trade_tweets: ' + str(recent_trade_tweets))
    logging.info(f'trades: {trades_for_binance}')

    return trades_for_binance

def _to_price_feed(price_data):
    # Create a Pandas dataframe from the price data
    dataframe = pd.DataFrame(data=price_data,
                             columns=['open_time', 'open', 'high', 'low', 'close', 'volume'])
    # convert date str to datetime obj
    dataframe['open_time'] = dataframe['open_time'].apply(lambda x: datetime.fromtimestamp(x / 1000))

    return bt.feeds.PandasData(dataname=dataframe,
                               datetime='open_time', open = 'open', high = 'high',
                               low = 'low', close = 'close', volume = 'volume'
                               )


def main():
    init_logging()
    trades = get_recent_trades()
    logging.info('number of trades found: ' + str(len(trades)))

    # for trade in trades:
    if len(trades) == 0:
        raise Exception('No trades found')

    logging.info(f'running backtest for {len(trades)} trades')
    results = []
    for trade in trades:
        result = run_backtest_for_trade(trade)
        logging.info(f'winning: {result}')
        results.append(result)

    valid_results = [result is TradeOutcome.CANCELLED for result in results]
    logging.info(f'winning trades: {results.count(TradeOutcome.WIN)} / {len(valid_results)}')


def run_backtest_for_trade(trade: Trade) -> TradeResult:
    logging.info(f'testing following trade with backtrader: {trade}')
    binance_price_data = get_price_data_from_date(trade.date, trade.symbol)

    # if symbol is invalid price data will be empty
    if len(binance_price_data) == 0:
        return TradeResult(outcome=TradeOutcome.CANCELLED, change_factor=0)

    cleansed_price_data = cleanse_binance_klines(binance_price_data)
    logging.info(f'cleansed price_data ({len(cleansed_price_data)} candles): {cleansed_price_data}')

    pd_data = _to_price_feed(cleansed_price_data)

    # Initialize the backtest
    cerebro = bt.Cerebro()
    cerebro.adddata(pd_data)

    # Add the strategy to Cerebro
    cerebro.addstrategy(SimpleSymmetricStrategy, direction=trade.direction)
    start_portfolio_value = cerebro.broker.getvalue()
    logging.info(f"Start Portfolio Value: {start_portfolio_value}")

    # Run the backtest
    cerebro.run()

    # todo?: check if the strategy exited its main position
    # position_was_exited = len(cerebro.broker.getpositions()) == 0
    # if not position_was_exited:
    #     return TradeOutcome.CANCELLED

    # cerebro.plot()
    logging.info(f"Final Portfolio Value: {cerebro.broker.getvalue()}")
    is_winning_outcome = cerebro.broker.getvalue() > start_portfolio_value
    return TradeResult(
        outcome=TradeOutcome.WIN if is_winning_outcome else TradeOutcome.LOSS,
        change_factor=cerebro.broker.getvalue() / start_portfolio_value
    )

if __name__ == '__main__':
    main()