from typing import List

from trader_tweets.repository.binance_repository import binance_has_symbol
from trader_tweets.model.trade import Trade
from trader_tweets.tweet_parsing import symbols_that_dont_need_usd_suffix


def filter_out_trades_with_symbols_not_on_binance(trades: List[Trade]) -> List[Trade]:
    not_crypto_symbols = symbols_that_dont_need_usd_suffix
    after_manual_filtering = [trade for trade in trades if trade.symbol not in not_crypto_symbols]
    after_binance_filtering = [trade for trade in after_manual_filtering if binance_has_symbol(trade.symbol)]
    return after_binance_filtering