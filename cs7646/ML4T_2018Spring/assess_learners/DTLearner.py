"""
A simple wrapper for Decision Tree Learner.

Building Decision Tree Slides: http://quantsoftware.gatech.edu/images/4/4e/How-to-learn-a-decision-tree.pdf
"""

import numpy as np
import pandas as pd

class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        return 'vla6' # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        if(dataX.shape[0] == 1):
            # If the number of rows left is equal to the leaf size, return
            pass
            # return [leaf,  data.y, NA, NA]
        if(np.unique(dataY).shape[0] == 1):
            # If all values of Y are the same, then make a leaf and return
            pass
            # return [leaf,  data.y, NA, NA]
        else:
            # Else Recursively build a tree

            # Determine best feature i to split on based on correlation
            print('Feature with the highest correlation is')
            corr = np.corrcoef(dataX, dataY, rowvar=False)
            corr_coef = corr[:, -1][0:-1]
            i = np.argmax(corr_coef)
            print(i)
            
            # Split the values based on median
            SplitVal =  data[:, i].median()
            lefttree =  addEvidence(data[data[:, i] <= SplitVal])
            righttree = addEvidence(data[data[:, i] > SplitVal])
            root = [i, SplitVal, 1, lefttree.shape[0] + 1]
            return  (append(root, lefttree, righttree))


        # LR Example: slap on 1s column so linear regression finds a constant term
        # LR Example: newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
        # LR Example: newdataX[:,0:dataX.shape[1]]=dataX

        # build and save the model
        # self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)
        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
