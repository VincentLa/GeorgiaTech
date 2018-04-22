"""
Strategy Learner -- Manual Strategy

Code implementing a ManualStrategy object (your manual strategy).
It should implement testPolicy() which returns a trades data frame (see below).
The main part of this code should call marketsimcode as necessary to generate the plots used in the report.
"""
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
# from marketsimcode import compute_portvals


def compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005):
    """
    Compute Portfolio Values in the original way.
    """
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


def bollinger_bands(df, stocks=['JPM'], window=20):
    """
    """
    # Compute Rolling mean using a 20 day window
    # Compute Rolling std using a 20 day window
    stock = stocks[0]
    rm = pd.rolling_mean(df[stock], window=window)
    rm_std = pd.rolling_std(df[stock], window=window)
    upper_band = rm + rm_std * 2
    lower_band = rm - rm_std * 2

    return upper_band, lower_band


def testPolicy(symbol="JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv=100000):
    """
    Do Stuff
    """
    prices = get_data([symbol], pd.date_range(sd, ed))

    # Normalize data
    prices = normalize_data(prices)

    # Calculate Bollinger Bands
    upper_band, lower_band = bollinger_bands(prices)  # These are series

    # Iterate through rows to find the optimal trades
    num_rows = prices.shape[0]
    dates = list(prices.index)
    symbols = [symbol] * num_rows
    orders = ['BUY']
    shares = [1000]
    current_position = 1000
    for i in range(1, num_rows):
        today_price = prices.ix[i][symbol]
        lower_bollinger = lower_band.ix[i]
        upper_bollinger = upper_band.ix[i]

        # If price is less than or equal to lower band, buy until position of +1000
        if today_price <= lower_bollinger:
            num_shares = 1000 - current_position
            orders.append('BUY')
            shares.append(num_shares)
            current_position = current_position + num_shares
        elif today_price >= upper_bollinger:
            num_shares = 1000 + current_position
            orders.append('SELL')
            shares.append(num_shares)
            current_position = current_position - num_shares
        else:
            orders.append('BUY')
            shares.append(0)

    df_trades = pd.DataFrame({
        'Date': dates,
        'Symbol': symbols,
        'Order': orders,
        'Shares': shares,
    })
    return df_trades


def assess_manual_strategy(
        plot_title='./in_sample_manual_strategy.png',
        symbol='JPM',
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 12, 31),
        sv=100000):
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
    # Creating benchmark orders DF
    prices = get_data([symbol], pd.date_range(sd, ed))
    dates = list(prices.index)
    symbols = [symbol] * len(dates)
    orders = ['BUY'] * len(dates)
    shares = [0] * len(dates)
    shares[0] = 1000  # On first date buy 1000 shares of JPM

    manual_policy_orders = testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    long_entry_points = []
    short_entry_points = []
    for date, row in manual_policy_orders.iterrows():
        if row.Shares > 0:
            if row.Order == 'BUY':
                long_entry_points.append(row.Date)
            if row.Order == 'SELL':
                short_entry_points.append(row.Date)

    benchmark_orders = pd.DataFrame({
        'Date': dates,
        'Symbol': symbols,
        'Order': orders,
        'Shares': shares,
    })

    manual_vals = compute_portvals(orders=manual_policy_orders, start_val=sv, commission=9.95, impact=0.005)
    benchmark_vals = compute_portvals(orders=benchmark_orders, start_val=sv, commission=9.95, impact=0.005)

    manual_cum_ret, manual_std_daily_ret, manual_avg_daily_ret = get_portfolio_stats(manual_vals)
    bench_cum_ret, bench_std_daily_ret, bench_avg_daily_ret = get_portfolio_stats(benchmark_vals)

    # Print Portfolio Performance in Text
    print('Cumulative Returns; Manual Portfolio: ', np.round(manual_cum_ret[0], 5))
    print('stdev of daily returns; Manual Portfolio: ', np.round(manual_std_daily_ret[0], 5))
    print('mean of daily returns; Manual portfolio is: ', np.round(manual_avg_daily_ret[0], 5))

    print('Cumulative Returns; Benchmark Portfolio is: ', np.round(bench_cum_ret[0], 5))
    print('stdev of daily returns; Benchmark Portfolio is: ', np.round(bench_std_daily_ret[0], 5))
    print('mean of daily returns; Benchmark Portfolio is: ', np.round(bench_avg_daily_ret[0], 5))

    # Create Portfolio Performance in Graph Form
    # First normalize to 1
    manual_vals = normalize_data(manual_vals)
    benchmark_vals = normalize_data(benchmark_vals)

    ax = manual_vals['portfolio_value'].plot(
        title='Portfolio Values Comparison', label='Manual Portfolio', color='black')

    # Add Benchmark to same plot
    benchmark_vals['portfolio_value'].plot(label='Benchmark Portfolio', ax=ax, color='blue')

    # Add Long and Short Values
    # for l in long_entry_points:
    #     ax.axvline(x=l, color='green', linestyle='--')
    # for s in short_entry_points:
    #     ax.axvline(x=s, color='red', linestyle='--')

    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value")
    ax.legend(loc='upper left')
    plt.savefig(plot_title)

    plt.cla()
    plt.clf()
    plt.close()


def main():
    """
    Do Stuff
    """
    in_sample_sd = dt.datetime(2008, 1, 1)
    in_sample_ed = ed=dt.datetime(2009, 12, 31)
    out_of_sample_sd = dt.datetime(2010, 1, 1)
    out_of_sample_ed = dt.datetime(2011, 12, 31)

    # Assess In Sample Manual Strategy
    print('Assessing In Sample Manual Strategy')
    assess_manual_strategy(
        plot_title='./in_sample_manual_strategy.png',
        symbol='JPM',
        sd=in_sample_sd,
        ed=in_sample_ed,
        sv=100000)

    # Assess Out of Sample Manual Strategy
    print('Assessing Out of Sample Manual Strategy')
    assess_manual_strategy(
        plot_title='./out_of_sample_manual_strategy.png',
        symbol='JPM',
        sd=out_of_sample_sd,
        ed=out_of_sample_ed,
        sv=100000)

if __name__ == "__main__":
    main()
