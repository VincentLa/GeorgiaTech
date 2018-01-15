"""
Analyze a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved

Run by cd'ing into the directory containing analysis.py and typing the following in terminal:
PYTHONPATH=../:. python analysis.py

This will add the python path appropriately

Note on running the grading script see: http://quantsoftware.gatech.edu/ML4T_Software_Setup

To SSH into Georgia Tech's machine:
ssh -X vla6@buffet02.cc.gatech.edu

To SFTP copy stuff over:
scp -r ML4T_2018Spring/* vla6@buffet02.cc.gatech.edu:ML4T_2018Spring/

Note this Piazza post on saving images: https://piazza.com/class/jc95nj7xalax8?cid=65
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data


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
def assess_portfolio(sd=dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 1, 1), \
                     syms=['GOOG', 'AAPL', 'GLD', 'XOM'], \
                     allocs=[0.1, 0.2, 0.3, 0.4], \
                     sv=1000000, rfr=0.0, sf=252.0, \
                     gen_plot=False):

    # Step 1: Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY

    # Step 2: Normalize the prices according to the first day
    prices_all = normalize_data(prices_all)

    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Step 3, 4, 5, 6: Calculate daily portfolio value by finding the normalized allocation each day
    # Then, calculate portfolio statistics
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
        plt.savefig('./output/plot.png')

    # Add code here to properly compute end value
    ev = sv * (1 + cr)

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    # start_date = dt.datetime(2009, 1, 1)
    # end_date = dt.datetime(2010, 1, 1)
    # symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    # allocations = [0.2, 0.3, 0.4, 0.1]
    # start_val = 1000000
    # risk_free_rate = 0.0
    # sample_freq = 252

    # Example 1:
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    # Example 2:
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    allocations = [0.0, 0.0, 0.0, 1.0]

    # Example 3:
    start_date = dt.datetime(2010, 6, 1)
    end_date = dt.datetime(2010, 12, 31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd=start_date, ed=end_date,\
        syms=symbols, \
        allocs=allocations,\
        sv=start_val, \
        gen_plot=True)

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
    test_code()
