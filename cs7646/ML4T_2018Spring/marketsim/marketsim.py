"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved

Run by using
PYTHONPATH=../:. python marketsim.py
PYTHONPATH=../:. python grade_marketsim.py

Using https://www.youtube.com/watch?v=TstVUVbu-Tk as a guide

Extra Point: https://www.youtube.com/watch?v=TstVUVbu-Tk 1:03:00
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
    orders.reset_index(inplace=True)

    # Get Start and End Date
    start_date = orders.Date.min()
    end_date = orders.Date.max()
    # start_date = dt.date(2011, 1, 10)
    # end_date = dt.date(2011, 12, 20)

    di = {'BUY': 1, 'SELL': -1}
    orders['order_direction'] = orders.Order.map(di)
    orders['actual_shares'] = orders.Shares * orders.order_direction
    # If there are transactions that net each other on the same day, net them out
    orders_transformed = orders.groupby(['Date', 'Symbol'])['actual_shares'].sum().to_frame()
    orders_transformed.reset_index(inplace=True)
    orders_transformed = orders_transformed.pivot(
        index='Date', columns='Symbol', values='actual_shares')
    orders_transformed = orders_transformed.fillna(0)


    # Get all unique stocks in the orders file
    stocks = list(orders.Symbol.unique())

    # Read in Prices Data for all the stocks in the orders file
    prices = get_data(stocks, pd.date_range(start_date, end_date))
    prices = prices[stocks]  # remove SPY

    # Create a copy of the prices DF
    # 1. Fill all values with 0's (About 26:50 in YT Video)
    # 2. Fill in values. Each Stock column represents change in position. Cash column represents change in cash
    #    (About 28:00 in YT Video)
    trades = prices.copy()

    trades = trades.replace(trades, 0)
    trades.update(orders_transformed)
    trade_values = trades.multiply(prices)
    # -1 because the cash you get is "opposite" of the order
    # For example, if you buy 1000 shares, you lose -1000 shares worth of cash
    trades['cash'] = trade_values.sum(axis=1) * -1

    # Now compute portfolio value daily
    # The value for each day is cash plus the current value of equities.
    portvals = trades.copy()
    portvals = portvals.cumsum()

    # Add a Cash column for prices
    prices['cash'] = 1.0
    portvals = portvals.multiply(prices)
    portvals['portfolio_value'] = portvals.sum(axis=1)
    portvals = portvals[['portfolio_value']]
    portvals['portfolio_value'] = portvals.portfolio_value + start_val

    # rv = pd.DataFrame(index=portvals.index, data=portvals.as_matrix())

    # Create dataframe of Prices
    print('printing Trades')
    print(trades)
    print(trades.index)

    print('prices')
    print(prices)
    print(prices.index)

    # print('portvals')
    # print(portvals)

    # print('printing rv')
    # print(rv.head())

    print('printing orders')
    print(orders.head())
    print(orders_transformed.head())
    print(orders_transformed.index)

    # return rv
    return portvals


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-short.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
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
