"""
implementing a BestPossibleStrategy object (details below). It should implement testPolicy()
which returns a trades data frame (see below).

The main part of this code should call marketsimcode as necessary to generate the plots used in the report.

-- Use only the data provided for this course. You are not allowed to import external data.
-- For your report, trade only the symbol JPM. This will enable us to more easily compare results.
-- You may use data from other symbols (such as SPY) to inform your strategy.
-- The in sample/development period is January 1, 2008 to December 31 2009.
-- The out of sample/testing period is January 1, 2010 to December 31 2011.
-- Starting cash is $100,000.
-- Allowable positions are: 1000 shares long, 1000 shares short, 0 shares.
-- Benchmark: The performance of a portfolio starting with $100,000 cash, investing in 1000 shares of JPM and holding that position.
-- There is no limit on leverage.
-- Transaction costs for ManualStrategy: Commission: $9.95, Impact: 0.005.
-- Transaction costs for BestPossibleStrategy: Commission: $0.00, Impact: 0.00.
"""
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
from marketsimcode import compute_portvals


def normalize_data(df):
    """
    Helper function to normalize Stock data by dividing by first day

    Taken from: https://classroom.udacity.com/courses/ud501/lessons/3975568860/concepts/41007386010923
    """
    return df / df.iloc[0, :]


def get_portfolio_stats(portvals):
    """
    Get Portfolio Stats given a dataframe of Portvals

    Returns:
      cum_ret,
      std_daily_ret,
      avg_daily_ret
    """
    last_day = portvals.shape[0] - 1
    cum_ret = portvals.ix[last_day] / portvals.ix[0] - 1

    # Daily Return = daily_portfolio_value[t] / daily_portfolio_value[t - 1] - 1
    # Taken from: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41858589820923
    daily_return = portvals / portvals.shift(1) - 1

    # Average Daily Return
    avg_daily_ret = daily_return.mean()

    # Standard deviation of daily return
    std_daily_ret = daily_return.std()

    return cum_ret, std_daily_ret, avg_daily_ret


def testPolicy(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
    """
    Keyword Args:
      symbol: the stock symbol to act on
      sd: A datetime object that represents the start date
      ed: A datetime object that represents the end date
      sv: Start value of the portfolio

    Returns:
      df_trades: A data frame whose values represent trades for each day.
                 Legal values are +1000.0 indicating a BUY of 1000 shares,
                 -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating
                 NOTHING. Values of +2000 and -2000 for trades are also legal
                 so long as net holdings are constrained to -1000, 0, and 1000.
    """
    # Read and normalize Data
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = normalize_data(prices)

    # Iterate through rows to find the optimal trades
    num_rows = prices.shape[0]
    dates = list(prices.index)
    symbols = ['JPM'] * num_rows
    orders = []
    shares = []
    current_position = 0
    for i in range(num_rows - 1):
        today_price = prices.ix[i]['JPM']
        tomorrow_price = prices.ix[i + 1]['JPM']

        # If next day price is bigger, buy until position of +1000
        if tomorrow_price >= today_price:
            num_shares = 1000 - current_position
            orders.append('BUY')
            shares.append(num_shares)
            current_position = current_position + num_shares
        elif tomorrow_price < today_price:
            num_shares = 1000 + current_position
            orders.append('SELL')
            shares.append(num_shares)
            current_position = current_position - num_shares
    # On very last day, don't know what to do, so just buy nothing.
    orders.append('BUY')
    shares.append(0)

    df_trades = pd.DataFrame({
        'Date': dates,
        'Symbol': symbols,
        'Order': orders,
        'Shares': shares,
    })
    return df_trades


def main():
    """
    Provide a chart that reports:
      -- Benchmark (The performance of a portfolio starting with $100,000 cash,
                    investing in 1000 shares of JPM and holding that position.)
         normalized to 1.0 at the start: Blue line
      -- Value of the best possible portfolio (normalized to 1.0 at the start): Black line

    You should also report in text:
      -- Cumulative return of the benchmark and portfolio
      -- Stdev of daily returns of benchmark and portfolio
      -- Mean of daily returns of benchmark and portfolio
    """
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000

    # Creating benchmark orders DF
    prices = get_data([symbol], pd.date_range(sd, ed))
    dates = list(prices.index)
    symbols = ['JPM'] * len(dates)
    orders = ['BUY'] * len(dates)
    shares = [0] * len(dates)
    shares[0] = 1000  # On first date buy 1000 shares of JPM

    best_policy_orders = testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    print(prices.head(10))

    best_policy_orders.to_csv('best_policy_orders.csv')

    benchmark_orders = pd.DataFrame({
        'Date': dates,
        'Symbol': symbols,
        'Order': orders,
        'Shares': shares,
    })

    best_vals = compute_portvals(orders=best_policy_orders, start_val=sv, commission=0, impact=0)
    benchmark_vals = compute_portvals(orders=benchmark_orders, start_val=sv, commission=0, impact=0)

    best_cum_ret, best_std_daily_ret, best_avg_daily_ret = get_portfolio_stats(best_vals)
    bench_cum_ret, bench_std_daily_ret, bench_avg_daily_ret = get_portfolio_stats(benchmark_vals)

    # Print Portfolio Performance in Text
    print('The cumulative returns for the best portfolio is: ', best_cum_ret[0])
    print('The stdev of daily returns for the best portfolio is: ', best_std_daily_ret[0])
    print('The mean of daily returns for the best portfolio is: ', best_avg_daily_ret[0])

    print('The cumulative returns for the benchmark portfolio is: ', bench_cum_ret[0])
    print('The stdev of daily returns for the benchmark portfolio is: ', bench_std_daily_ret[0])
    print('The mean of daily returns for the benchmark portfolio is: ', bench_avg_daily_ret[0])

    # Create Portfolio Performance in Graph Form
    # First normalize to 1
    best_vals = normalize_data(best_vals)
    benchmark_vals = normalize_data(benchmark_vals)
    ax = best_vals['portfolio_value'].plot(
        title='Portfolio Values Comparison', label='Best Portfolio', color='black')

    # Add Benchmark to same plot
    benchmark_vals['portfolio_value'].plot(label='Benchmark Portfolio', ax=ax, color='blue')

    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value")
    ax.legend(loc='upper left')
    plt.savefig('./best_possible_strategy.png')


if __name__ == "__main__":
    main()


