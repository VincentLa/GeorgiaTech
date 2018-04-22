"""
Strategy Learner Experiment 1: http://quantsoftware.gatech.edu/Strategy_learner

Vincent La (vla6)

To run:
PYTHONPATH=../:. python experiment1.py

Using exactly the same indicators that you used in manual_strategy, compare your manual strategy
with your learning strategy in sample. Plot the performance of both strategies in sample along
with the benchmark. Trade only the symbol JPM for this evaluation. 
"""

import datetime as dt
import pandas as pd
import util as ut
import random
from dateutil import relativedelta

# import indicators as ind
import StrategyLearner as sl
import ManualStrategy as ms


def author():
    return 'vla6'


def main():
    """
    Do Stuff
    """
    in_sample_sd = dt.datetime(2008, 1, 1)
    in_sample_ed = ed=dt.datetime(2009, 12, 31)
    out_of_sample_sd = dt.datetime(2010, 1, 1)
    out_of_sample_ed = dt.datetime(2011, 12, 31)

    print('Assessing Manual Strategy Against Strategy Learner')
    # Manual Strategy
    manual_vals, benchmark_vals = ms.assess_manual_strategy()

    # Strategy Learner
    strategy_learner = sl.StrategyLearner()
    strategy_learner.addEvidence(symbol='JPM')
    strategy_learner_df_trades = strategy_learner.testPolicy(symbol='JPM')
    print(strategy_learner_df_trades.head())

if __name__=="__main__":
    main()
