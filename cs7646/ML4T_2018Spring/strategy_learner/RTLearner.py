"""
A simple wrapper for Random Tree Learner.

Building Decision Tree Slides: http://quantsoftware.gatech.edu/images/4/4e/How-to-learn-a-decision-tree.pdf
"""

import numpy as np
import pandas as pd

class RTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = np.array([])  # Before training set tree to empty array

    def author(self):
        return 'vla6' # replace tb34 with your Georgia Tech username

    def buildTree(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values

        See https://www.youtube.com/watch?v=WVc3cjvDHhw for more information on building the tree
        """
        if(dataX.shape[0] <= self.leaf_size):
            # If the number of rows left is equal to the leaf size
            # Setting the feature to split on as -1 to signify no splits
            # Aggregate by taking the mean
            y_value = np.mean(dataY)
            return np.array([[-1,  y_value, np.nan, np.nan]])
        if(np.unique(dataY).shape[0] == 1):
            # If all values of Y are the same, then make a leaf and return
            y_value = np.unique(dataY)
            return np.array([[-1,  y_value, np.nan, np.nan]])
        else:
            # Else Recursively build a tree
            # Instead of selecting feature based on correlation, select based on random int generator
            i = np.random.randint(low=0, high=dataX.shape[1])

            # Split the values based on median, unless the median = the max or the min then take the average
            # This is because if the median equals either the median or max it doesn't actually split the data
            if(np.median(dataX[:, i]) == np.max(dataX[:, i]) or np.median(dataX[:, i]) == np.min(dataX[:, i])):
                SplitVal = np.mean(dataX[:, i])
            else:
                SplitVal =  np.median(dataX[:, i])
            lefttree =  self.buildTree(dataX[dataX[:, i] <= SplitVal], dataY[dataX[:, i] <= SplitVal])
            righttree = self.buildTree(dataX[dataX[:, i] > SplitVal], dataY[dataX[:, i] > SplitVal])
            
            # Left tree begins in the next row of the matrix. That's why third parameter is equal to 1
            root = np.array([[i, SplitVal, 1, lefttree.shape[0] + 1]])
            return (np.concatenate((root, lefttree, righttree), axis=0))

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values

        See https://www.youtube.com/watch?v=WVc3cjvDHhw for more information on building the tree
        """
        self.tree = self.buildTree(dataX, dataY)

    def query_single(self, point):
        """
        For a single array, query the tree and return the test Y
        """
        traverse_tree_index = 0
        while traverse_tree_index < self.tree.shape[0]:
            decision_row = self.tree[traverse_tree_index]
            factor_index = int(decision_row[0])
            split_value = decision_row[1]
            left_tree_index = decision_row[2]
            right_tree_index = decision_row[3]
            if factor_index < 0:
                """Then the split_value is actually leaf node"""
                return split_value
            elif(point[factor_index] <= split_value):
                """If not a leaf node, and the chosen factor is less than Split"""
                traverse_tree_index += int(left_tree_index)
            else:
                """Else, traverse to the right tree"""
                traverse_tree_index += int(right_tree_index)    


    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        testY = np.array([])
        for point in points:
            testY = np.append(testY, self.query_single(point))
        return testY

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
