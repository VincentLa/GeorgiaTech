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

import indicators as ind
import RTLearner as rt


def author():
    return 'vla6'


def main():
    """
    Do Stuff
    """
    strategy_learner = StrategyLearner()
    strategy_learner.addEvidence(symbol='JPM')
    strategy_learner.testPolicy(symbol='JPM')


if __name__=="__main__":
    main()
