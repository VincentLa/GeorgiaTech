"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
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

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 

        # add your code to do learning here

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

if __name__=="__main__":
    print "One does not simply think up a strategy"
