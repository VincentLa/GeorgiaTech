"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved

Run by using
PYTHONPATH=../:. python marketsim.py
PYTHONPATH=../:. python grade_marketsim.py

Using https://www.youtube.com/watch?v=TstVUVbu-Tk as a guide

Extra Point: https://www.youtube.com/watch?v=TstVUVbu-Tk 1:03:00
June 15th, 2011, ignore all orders.
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return 'vla6'


def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input

    # Read in Orders file
    orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])

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


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-short.csv"
    orders = pd.read_csv(of, index_col='Date', parse_dates=True, na_values=['nan'])

    # Get Start and End Date
    start_date = orders.index.min()
    end_date = orders.index.max()

    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    last_day = portvals.shape[0] - 1
    cum_ret = portvals[last_day] / portvals[0] - 1

    # Daily Return = daily_portfolio_value[t] / daily_portfolio_value[t - 1] - 1
    # Taken from: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41858589820923
    daily_return = portvals / portvals.shift(1) - 1
    
    # Average Daily Return
    avg_daily_ret = daily_return.mean()

    # Standard deviation of daily return
    std_daily_ret = daily_return.std()

    rfr = 0
    sf = 252
    sharpe_ratio = (daily_return - rfr).mean() / (daily_return - rfr).std()
    sharpe_ratio *= np.sqrt(sf)

    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
