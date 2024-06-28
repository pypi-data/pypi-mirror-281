import logging
import os
from datetime import datetime, timedelta

import diskcache

from trader_tweets.service.cache_service import CACHE_DIR

api_key = os.environ['BINANCE_API_KEY']
api_secret = os.environ['BINANCE_SECRET_KEY']

from binance import Client
client = Client(api_key, api_secret)

cache = diskcache.Cache(CACHE_DIR)


@cache.memoize()
def get_price_data_from_date(date: datetime, symbol: str):
    # get the hourly price of the cryptocurrency ${symbol} from the binance klines api
    # starting from ${date} and going for a further 1 week
    # api_key = os.environ['BINANCE_API_KEY']

    interval = Client.KLINE_INTERVAL_4HOUR

    end_time = date + timedelta(days=60)
    print(f'Getting price data for {symbol} from {date} to {end_time}')

    start_time_ms = int(date.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    try:
        return client.get_historical_klines(symbol=symbol,
                                            interval=interval,
                                            start_str=start_time_ms,
                                            end_str=end_time_ms)
    except Exception as e:
        logging.debug(f'Exception: {e}')
        if 'APIError(code=-1121): Invalid symbol.' in str(e):
            logging.error(f'Invalid symbol: {symbol}')
            return []


@cache.memoize()
def binance_has_symbol(symbol: str):
    # check if binance has a symbol
    # if it doesn't, then we can't backtest it
    symbol = client.get_symbol_info(symbol)
    return symbol is not None