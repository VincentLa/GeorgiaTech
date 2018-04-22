"""
Vincent La
Georgia Tech ID: vla6

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

Note FYI on Format of df_trades: https://piazza.com/class/jc95nj7xalax8?cid=1638.
Also see https://piazza.com/class/jc95nj7xalax8?cid=1581
"""

import datetime as dt
import pandas as pd
import util as ut
import random
from dateutil import relativedelta

import indicators as ind
import RTLearner as rt


def map_y_values(ret, YBUY=0.01, YSELL=-0.01):
    if ret > YBUY:
        return 1  # LONG
    elif ret < YSELL:
        return -1  # SHORT
    else:
        return 0 # CASH


class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.learner = rt.RTLearner(leaf_size=5, verbose = False)

    def author(self):
        return 'vla6' # replace tb34 with your Georgia Tech username

    def addEvidence(self, symbol = "IBM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 10000): 
        """
        Learner will be provided with a stock symbol and time period.
        """
        # As per https://piazza.com/class/jc95nj7xalax8?cid=939, can look back n days before start date for run-up
        # for technical indicators like rolling mean.
        n = 20  # This is the window we use (hardcoded)
        lookbacksd = sd - relativedelta.relativedelta(days=30)
        lookforwarded = ed + relativedelta.relativedelta(days=30)

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(lookbacksd, lookforwarded)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        feature_df = prices.copy()
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices
  
        # example use with new colname 
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        if self.verbose: print volume

        # Adding Code to do Learning Here

        ############################################################################################
        # Construct Features
        ############################################################################################
        # First, compute indicators and add as X variables. There should be 3 - 5 features, each corresponding
        # to the indicator
        lower_bollinger_band, upper_bollinger_band = ind.bollinger_bands(df=prices, stocks=syms)
        sma = ind.sma(df=prices, stocks=syms)
        roc = ind.rate_of_change(df=prices, stocks=syms)
        ewma = ind.exponential_weighted_moving_average(df=prices, stocks=syms)

        feature_df['lower_bollinger_band'] = lower_bollinger_band
        feature_df['upper_bollinger_band'] = upper_bollinger_band
        feature_df['sma'] = sma
        feature_df['roc'] = roc
        feature_df['ewma'] = ewma

        # Second, compute the Y values for each date.
        # Also adding in impact of impact.
        YBUY = 0.04 + self.impact
        YSELL = -0.04 - self.impact
        ret = (feature_df[symbol].shift(-1 * n) / feature_df[symbol]) - 1.0
        feature_df['ret'] = ret
        feature_df['y'] = feature_df.ret.apply(map_y_values, args=(YBUY, YSELL))
        feature_df = feature_df.loc[feature_df.index >= sd]
        feature_df = feature_df.loc[feature_df.index <= ed]
        feature_df.drop(['ret'], axis=1, inplace=True)
        # print(feature_df.head(5))

        ############################################################################################
        # Use RTLearner to Do Learning
        ############################################################################################
        Xcols = list(feature_df.columns)
        Xcols.remove('y')
        ycols = 'y'
        trainX = feature_df[Xcols].as_matrix()
        trainY = feature_df[ycols]

        self.learner.addEvidence(trainX, trainY)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", sd=dt.datetime(2009,1,1), ed=dt.datetime(2010,1,1), sv = 10000):
        """
        Returns:
          df_trades: A data frame whose values represent trades for each day. Legal values are +1000.0
                     indicating a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares,
                     and 0.0 indicating NOTHING. Values of +2000 and -2000 for trades are also legal
                     when switching from long to short or short to long so long as net holdings are
                     constrained to -1000, 0, and 1000.
        """

        # here we build a fake set of trades
        # your code should return the same sort of data
        n = 20  # This is the window we use (hardcoded)
        lookbacksd = sd - relativedelta.relativedelta(days=30)
        lookforwarded = ed + relativedelta.relativedelta(days=30)

        syms=[symbol]
        dates = pd.date_range(lookbacksd, lookforwarded)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        feature_df = prices.copy()
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades = trades.loc[trades.index >= sd]
        trades = trades.loc[trades.index <= ed]
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        trades.values[:,:] = 0 # set them all to nothing
        trades.values[0,:] = 1000 # add a BUY at the start
        # trades.values[40,:] = -1000 # add a SELL 
        # trades.values[41,:] = 1000 # add a BUY 
        # trades.values[60,:] = -2000 # go short from long
        # trades.values[61,:] = 2000 # go long from short
        # trades.values[-1,:] = -1000 #exit on the last day
        ############################################################################################
        # Constructing test feature DF -- should be exact copy of code
        ############################################################################################
        lower_bollinger_band, upper_bollinger_band = ind.bollinger_bands(df=prices, stocks=syms)
        sma = ind.sma(df=prices, stocks=syms)
        roc = ind.rate_of_change(df=prices, stocks=syms)
        ewma = ind.exponential_weighted_moving_average(df=prices, stocks=syms)

        feature_df['lower_bollinger_band'] = lower_bollinger_band
        feature_df['upper_bollinger_band'] = upper_bollinger_band
        feature_df['sma'] = sma
        feature_df['roc'] = roc
        feature_df['ewma'] = ewma
        feature_df = feature_df.loc[feature_df.index >= sd]
        feature_df = feature_df.loc[feature_df.index <= ed]

        ############################################################################################
        # Adding our own trades dataframe
        ############################################################################################
        # Use the learner to output predictions
        points = feature_df.as_matrix()
        testY = self.learner.query(points=points)

        df_trades = trades.copy()

        current_position = 1000
        trades = [1000]
        for i in range(1, len(testY)):
            if testY[i] == 1:
                trade = 1000 - current_position
            elif testY[i] == -1:
                trade = -1000 - current_position
            else:
                trade = 0
            current_position += trade
            trades.append(trade)
        df_trades['Shares'] = trades
        df_trades = df_trades[['Shares']]

        if self.verbose: print type(df_trades) # it better be a DataFrame!
        if self.verbose: print df_trades
        if self.verbose: print prices_all
        return df_trades


def main():
    """
    Do Stuff
    """
    strategy_learner = StrategyLearner()
    strategy_learner.addEvidence(symbol='JPM')
    strategy_learner.testPolicy(symbol='JPM')


if __name__=="__main__":
    main()
