import logging

import backtrader as bt

from trader_tweets.model.trade import Direction

# first strategy:
# 1) enter position at first candle
# 2) stop loss and take profit prices are calculated based on the entry price and
STOP_LOSS_BELOW_ENTRY = .1 # 10% below
TAKE_PROFIT_ABOVE_ENTRY = .1 # 10% above
TRADE_SIZE_SCALAR = 0.5 # proportion of portfolio to trade
class SimpleSymmetricStrategy(bt.Strategy):
    params = (('direction', Direction.LONG),)

    def init(self):
        pass

    def __init__(self):
        self.data_close = self.datas[0].close
        self.entry_price = None
        self.entry_trade_fee = None
        self.stop_loss_price = None
        self.take_profit_price = None
        self.has_sold = False

        portfolio_size = self.broker.get_cash()
        self.trade_size = portfolio_size * TRADE_SIZE_SCALAR
        logging.info('trade_size: ' + str(self.trade_size))

    def next(self):
        current_price = self.data_close[0]

        # this strategy ends once the position is closed
        if self.has_sold:
            return

        if not self.position:
            self.enter_trade(current_price)

        else:
            self._exit_trade_if_stop_loss_or_take_profit()

    def notify_order(self, order):
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            logging.info('Order status: ' + str(order.getstatusname()))
            return

        if order.status in [bt.Order.Completed]:
            if order.isbuy():
                self.entry_price = order.executed.price
                self.entry_trade_fee = order.executed.comm

        if order.isbuy():
            logging.info('BUY  {}  Size: {:.2f}  Price: {:.2f}'.format(order.data._name, order.executed.size,
                                                                   order.executed.price))
        else:
            logging.info('SELL {}  Size: {:.2f}  Price: {:.2f}'.format(order.data._name, order.executed.size,
                                                                   order.executed.price))


        if order.status in [bt.Order.Canceled, bt.Order.Margin, bt.Order.Rejected]:
            # logging.info the status of the order in english
            logging.info('Order failed with status: ' + str(order.getstatusname()))

    def enter_trade(self, current_price):
        # logging.info('buying at price:', str(buy_price), 'size:', position_size)
        position_size = self.trade_size / current_price

        if self.params.direction == Direction.LONG:
            self.buy(price=current_price, size=position_size)
        elif self.params.direction == Direction.SHORT:
            # borrow and sell
            self.sell(price=current_price, size=position_size)
        else:
            raise Exception('Invalid direction: ' + str(self.params.direction))

        self.entry_price = current_price
        self.stop_loss_price = self.entry_price * (1 - STOP_LOSS_BELOW_ENTRY)
        self.take_profit_price = self.entry_price * (1 + TAKE_PROFIT_ABOVE_ENTRY)

    def _exit_trade_if_stop_loss_or_take_profit(self):
        if self.data_close[0] <= self.stop_loss_price:
            self.close(price=self.stop_loss_price)
            self.has_sold = True
        elif self.data_close[0] >= self.take_profit_price:
            self.close(price=self.take_profit_price)
            self.has_sold = True
