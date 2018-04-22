"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch

See http://quantsoftware.gatech.edu/Strategy_learner for instructions
See http://quantsoftware.gatech.edu/Classification_Trader_Hints for hints

In my ManualStrategy implementation, I used N = 20. For consistency sake (see https://piazza.com/class/jc95nj7xalax8?cid=1528)
I will use N = 20 in this example as well.

Steps
1. Convert from Regression Tree to Classification Tree by taking majority rule (see https://piazza.com/class/jc95nj7xalax8?cid=1546 for somewhat helpful post)
2. As X values, for each day, compute the technical indicators as used in ManualStrategy project
3. For Y values, these should be based on N = 20 day return (see note above). As taken from the hints,
   Let y_buy be a constant such that if N day return exceeds a certain value then buy
   Let y_sell be a constant such that if N day return goes below a certain value then sell
   In all other cases, set y to 0 (or "Cash")

    Pseudocode for creating Y values
    ret = (price[t+N]/price[t]) - 1.0
    if ret > YBUY:
        Y[t] = +1 # LONG
    else if ret < YSELL:
        Y[t] = -1 # SHORT
    else:
        Y[t] = 0 # CASH

To run:
PYTHONPATH=../:. python StrategyLearner.py
"""

import datetime as dt
import pandas as pd
import util as ut
import random

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact

    def author(self):
        return 'vla6' # replace tb34 with your Georgia Tech username

    def addEvidence(self, symbol = "IBM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), sv = 10000): 
        """
        Learner will be provided with a stock symbol and time period.

        Returns:
          df_trades: A data frame whose values represent trades for each day. Legal values are +1000.0
                     indicating a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares,
                     and 0.0 indicating NOTHING. Values of +2000 and -2000 for trades are also legal
                     when switching from long to short or short to long so long as net holdings are
                     constrained to -1000, 0, and 1000.
        """
        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices
  
        # example use with new colname 
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        if self.verbose: print volume

        # add your code to do learning here
        print(prices.head())

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        trades.values[:,:] = 0 # set them all to nothing
        trades.values[0,:] = 1000 # add a BUY at the start
        trades.values[40,:] = -1000 # add a SELL 
        trades.values[41,:] = 1000 # add a BUY 
        trades.values[60,:] = -2000 # go short from long
        trades.values[61,:] = 2000 # go long from short
        trades.values[-1,:] = -1000 #exit on the last day
        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        return trades


def main():
    """
    Do Stuff
    """
    strategy_learner = StrategyLearner()
    strategy_learner.addEvidence(symbol='JPM')


if __name__=="__main__":
    main()
