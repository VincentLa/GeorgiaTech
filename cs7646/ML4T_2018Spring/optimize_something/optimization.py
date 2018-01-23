"""MC1-P2: Optimize a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved

See this helpful post on unuseful error in SciPy: https://piazza.com/class/jc95nj7xalax8?cid=189
Udacity Lesson for Optimizers Starts Here: https://classroom.udacity.com/courses/ud501/lessons/4351588706/concepts/43677793140923
"""

import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo


def normalize_data(df):
    """
    Helper function to normalize Stock data by dividing by first day

    Taken from: https://classroom.udacity.com/courses/ud501/lessons/3975568860/concepts/41007386010923
    """
    return df / df.iloc[0, :]


def compute_daily_portfolio_value(df_prices, syms, allocs):
    """
    Helper function to compute daily portfolio values.

    Keyword Args:
        df_prices: DataFrame containing time series data of prices
    """
    df_prices['daily_portfolio_value'] = 0
    for s, a in zip(syms, allocs):
        df_prices['daily_portfolio_value'] += df_prices[s] * a
    return df_prices


def compute_sddr(allocs, df_prices, rfr=0.0, sf=252.0):
    """
    Helper function to compute Standard Deviation of Daily Return.

    Keyword Args:
        df_prices: DataFrame containing time series data of prices
        allocs: A list of allocations to the stocks, must sum to 1.
                This is what we are trying to optimize!
        rfr: The risk free return per sample period for the entire date range. We assume no changes
        sf: Sampling frequency per year

    Returns:
        sddr: Standard deviation of daily return
    """
    syms = list(df_prices.columns)
    df_prices = compute_daily_portfolio_value(df_prices, syms, allocs)
    last_day = df_prices.shape[0] - 1

    # Cumulative Return = daily_portfolio_value[t] / daily_portfolio_value[0] - 1
    cr = df_prices.daily_portfolio_value.iloc[last_day] / df_prices.daily_portfolio_value.iloc[0] - 1

    # Daily Return = daily_portfolio_value[t] / daily_portfolio_value[t - 1] - 1
    # Taken from: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41858589820923
    df_prices['daily_return'] = df_prices.daily_portfolio_value /\
        df_prices.daily_portfolio_value.shift(1) - 1

    # Average Daily Return
    adr = df_prices.daily_return.mean()

    # Standard deviation of daily return
    sddr = df_prices.daily_return.std()

    # Compute Sharp Ratio (mean of difference of daily return and rfr) / (std of differences of daily return and rfr)
    # https://classroom.udacity.com/courses/ud501/lessons/4242038556/concepts/41998985500923
    # https://classroom.udacity.com/courses/ud501/lessons/4242038556/concepts/41998985510923
    sr = (df_prices.daily_return - rfr).mean() / (df_prices.daily_return - rfr).std()
    sr *= np.sqrt(sf)

    return sddr


def compute_portfolio_stats(df_prices, allocs=[0.1, 0.2, 0.3, 0.4], rfr=0.0, sf=252.0):
    """
    Helper function to compute portfolio stats.

    Keyword Args:
        df_prices: DataFrame containing time series data of prices
        allocs: A list of allocations to the stocks, must sum to 1
        rfr: The risk free return per sample period for the entire date range. We assume no changes
        sf: Sampling frequency per year

    Returns:
        cr: Cumulative return
        adr: Average Daily Return
        sddr: Standard deviation of daily return
        sr: Sharpe Ratio
    """
    syms = list(df_prices.columns)
    df_prices = compute_daily_portfolio_value(df_prices, syms, allocs)
    last_day = df_prices.shape[0] - 1

    # Cumulative Return = daily_portfolio_value[t] / daily_portfolio_value[0] - 1
    cr = df_prices.daily_portfolio_value.iloc[last_day] / df_prices.daily_portfolio_value.iloc[0] - 1

    # Daily Return = daily_portfolio_value[t] / daily_portfolio_value[t - 1] - 1
    # Taken from: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41858589820923
    df_prices['daily_return'] = df_prices.daily_portfolio_value /\
        df_prices.daily_portfolio_value.shift(1) - 1
    # df_prices['daily_return'].iloc[0] = 0  # set daily returns for first day to 0 Perhaps don't need since we're calculating statistics excluding first day?

    # Average Daily Return
    adr = df_prices.daily_return.mean()

    # Standard deviation of daily return
    sddr = df_prices.daily_return.std()

    # Compute Sharp Ratio (mean of difference of daily return and rfr) / (std of differences of daily return and rfr)
    # https://classroom.udacity.com/courses/ud501/lessons/4242038556/concepts/41998985500923
    # https://classroom.udacity.com/courses/ud501/lessons/4242038556/concepts/41998985510923
    sr = (df_prices.daily_return - rfr).mean() / (df_prices.daily_return - rfr).std()
    sr *= np.sqrt(sf)

    return df_prices, cr, adr, sddr, sr


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY

    # Step 2: Normalize the prices according to the first day
    prices_all = normalize_data(prices_all)

    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    # See https://classroom.udacity.com/courses/ud501/lessons/4351588706/concepts/43677793280923 as a reference
    # Initialize Allocations to 1/n as suggested by the assignment
    init_allocs = np.repeat(1.0 / len(syms), len(syms))
    bounds = ((0, 1),) * len(syms)
    constraints = (
                      # First constraint is that allocations has to sum to 0
                      {
                          'type': 'eq',
                          'fun': lambda inputs: 1.0 - np.sum(inputs)
                      }
                   )
    results = spo.minimize(compute_sddr, init_allocs, args=(prices,),
                          bounds=bounds, constraints=constraints, method='SLSQP', options={'disp': True})
    allocs = results.x

    # Pass in the optimal allocs into compute_portfolio_stats
    prices, cr, adr, sddr, sr = compute_portfolio_stats(prices, allocs)

    # Get daily portfolio value
    port_val = prices.daily_portfolio_value

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)

        plt.figure(figsize=(7, 4))
        plt.plot(df_temp['Portfolio'], color='b', label='Portfolio')
        plt.plot(df_temp['SPY'], color='g', label='SPY')
        plt.grid(True)
        plt.legend(loc=0)
        plt.xlabel('Date')
        plt.ylabel('Normalized Price')
        plt.title('Daily portfolio value and SPY')
        plt.show()
        plt.savefig('./plot.png')

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    # Default test case is
    # Start Date: 2008-06-01, End Date: 2009-06-01, Symbols: ['IBM', 'X', 'GLD']


    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
