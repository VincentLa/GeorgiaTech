"""
An improved version of your marketsim code that accepts a "trades" data frame (instead of a file).
More info on the trades data frame below.
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return 'vla6'


def compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005):
    """Compute Portfolio Values"""
    # Read in Orders file
    orders.set_index('Date', inplace=True)

    # Get Start and End Date
    start_date = orders.index.min()
    end_date = orders.index.max()

    di = {'BUY': 1, 'SELL': -1}
    orders['order_direction'] = orders.Order.map(di)
    orders['actual_shares'] = orders.Shares * orders.order_direction

    # Get all unique stocks in the orders file
    stocks = list(orders.Symbol.unique())

    # Read in Prices Data for all the stocks in the orders file
    prices = get_data(stocks, pd.date_range(start_date, end_date))
    prices = prices[stocks]  # remove SPY
    prices['cash'] = 1.0

    # Create a copy of the prices DF
    # 1. Fill all values with 0's (About 26:50 in YT Video)
    # 2. Fill in values. Each Stock column represents change in position. Cash column represents change in cash
    #    (About 28:00 in YT Video)
    trades = prices.copy()
    trades = trades.replace(trades, 0)

    # Loop through orders DF to update Trades
    for index, row in orders.iterrows():
        ticker = row.Symbol
        price = prices.loc[index, ticker]

        # Extra Point: https://www.youtube.com/watch?v=TstVUVbu-Tk 1:03:00
        # June 15th, 2011, ignore all orders.
        if index != dt.datetime(2011, 6, 15, 0, 0, 0):
            trades.loc[index, ticker] += row.actual_shares
            if row.Order == 'BUY':
                new_price = price * (1 + impact)
                trades.loc[index, 'cash'] += (-1 * new_price * row.actual_shares) - commission
            if row.Order == 'SELL':
                new_price = price * (1 - impact)
                trades.loc[index, 'cash'] += (-1 * new_price * row.actual_shares) - commission

    # Now compute portfolio value daily
    # The value for each day is cash plus the current value of equities.
    portvals = trades.copy()
    portvals = portvals.cumsum()

    portvals = portvals.multiply(prices)
    portvals['portfolio_value'] = portvals.sum(axis=1)
    portvals = portvals[['portfolio_value']]

    # Adding the starting value at the end
    # Shouldn't matter in this case that we add it in the end. Even if we assume 0 cash at the beginning
    # Because we don't have to worry about leverage it's fine.
    portvals['portfolio_value'] = portvals.portfolio_value + start_val

    return portvals
