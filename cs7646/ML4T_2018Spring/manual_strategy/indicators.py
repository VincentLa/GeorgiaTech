"""
Your code that implements your indicators as functions that operate on dataframes.
The "main" code in indicators.py should generate the charts that illustrate your
indicators in the report.

See Time Series Lecture: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41444292690923

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
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def normalize_data(df):
    """
    Helper function to normalize Stock data by dividing by first day

    Taken from: https://classroom.udacity.com/courses/ud501/lessons/3975568860/concepts/41007386010923
    """
    return df / df.iloc[0, :]


def bollinger_bands(df):
    """
    """
    pass


def sma(df):
    """
    Calculate Simple Moving Average
    """
    pass

def rate_of_change(df):
    """
    REMOVE THESE BEFORE SUBMITTING
    https://www.quantinsti.com/blog/build-technical-indicators-in-python/#roc
    """
    pass


def create_indicators(stocks=['JPM'], start_date=dt.date(2008, 1, 1), end_date=dt.date(2009, 1, 1)):
    """
    Develop and describe 3 technical indicators
    """
    prices = get_data(stocks, pd.date_range(start_date, end_date))

    # Normalize data
    prices = normalize_data(prices)

    print(prices.head())


def main():
    """
    Do Stuff: In particular produce charts
    """
    create_indicators()


if __name__ == "__main__":
    main()
