"""
Strategy Learner Experiment 2: http://quantsoftware.gatech.edu/Strategy_learner

Vincent La
Georgia Tech ID: vla6

To run:
PYTHONPATH=../:. python experiment2.py

Expand on Experiment 1 by adding in non-zero impact.
"""
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd
import util as ut
import random
from dateutil import relativedelta

# import indicators as ind
from marketsimcode import compute_portvals
import StrategyLearner as sl
import ManualStrategy as ms


def author():
    return 'vla6'


def map_order_values(x):
    if x >= 0:
        return 'BUY'
    else:
        return 'SELL'


def process_df_trades(df_trades, symbol='JPM'):
    """Process DF Trades from single column to fit marketsimcode"""
    df_trades.reset_index(inplace=True)
    df_trades = df_trades.rename(columns={'index': 'Date'})
    df_trades['Symbol'] = 'JPM'
    df_trades['Order'] = df_trades.Shares.apply(map_order_values)
    return df_trades


def normalize_data(df):
    """
    Helper function to normalize Stock data by dividing by first day

    Taken from: https://classroom.udacity.com/courses/ud501/lessons/3975568860/concepts/41007386010923
    """
    return df / df.iloc[0, :]


def main():
    """
    Do Stuff
    """
    in_sample_sd = dt.datetime(2008, 1, 1)
    in_sample_ed = ed=dt.datetime(2009, 12, 31)
    out_of_sample_sd = dt.datetime(2010, 1, 1)
    out_of_sample_ed = dt.datetime(2011, 12, 31)
    # Setting commission and impact to 0 as per: https://piazza.com/class/jc95nj7xalax8?cid=1474
    commission = 0
    impact = 0.1

    plot_title = './in_sample_strategy_comparison_impact_1.png'

    print('Assessing Manual Strategy Against Strategy Learner')
    # Manual Strategy
    manual_vals, benchmark_vals = ms.assess_manual_strategy(
        symbol='JPM', sd=in_sample_sd, ed=in_sample_ed, commission=commission, impact=impact)

    # Strategy Learner
    strategy_learner = sl.StrategyLearner(impact=impact)
    strategy_learner.addEvidence(symbol='JPM', sd=in_sample_sd, ed=in_sample_ed)
    strategy_learner_df_trades = strategy_learner.testPolicy(symbol='JPM', sd=in_sample_sd, ed=in_sample_ed)
    strategy_learner_orders = process_df_trades(strategy_learner_df_trades)
    strategy_learner_vals = compute_portvals(orders=strategy_learner_orders, commission=commission, impact=impact)
    strategy_learner_vals = normalize_data(strategy_learner_vals)

    # Compute Portfolio Values for Strategy Learner
    sl_cum_ret, sl_std_daily_ret, sl_avg_daily_ret = ms.get_portfolio_stats(strategy_learner_vals)
    # Print Portfolio Performance in Text
    print('Cumulative Returns; Strategy Learner Portfolio: ', np.round(sl_cum_ret[0], 5))
    print('stdev of daily returns; Strategy Learner Portfolio: ', np.round(sl_std_daily_ret[0], 5))
    print('mean of daily returns; Strategy Learner portfolio is: ', np.round(sl_avg_daily_ret[0], 5))

    # Making Plots
    ax = manual_vals['portfolio_value'].plot(
        title='Impact = {}'.format(impact), label='Manual Portfolio', color='black')

    # Adding strategy learner vals
    strategy_learner_vals['portfolio_value'].plot(label='Strategy Learner Portfolio', ax=ax, color='red')

    # Add Benchmark to same plot
    benchmark_vals['portfolio_value'].plot(label='Benchmark Portfolio', ax=ax, color='blue')

    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value")
    ax.legend(loc='upper left')
    ax.set_ylim(-1.5, 2.5)
    plt.savefig(plot_title)

    plt.cla()
    plt.clf()
    plt.close()

if __name__=="__main__":
    main()
