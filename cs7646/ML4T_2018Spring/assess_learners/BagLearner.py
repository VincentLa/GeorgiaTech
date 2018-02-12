"""
A simple wrapper for Bootstrap Aggregating.

Building Decision Tree Slides: http://quantsoftware.gatech.edu/images/4/4e/How-to-learn-a-decision-tree.pdf
"""

import numpy as np
import pandas as pd

class BagLearner(object):

    def __init__(self, learner, kwargs, bags, boost=False, verbose=False):
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []
        for i in range(0, self.bags):
            self.learners.append(learner(**kwargs))

    def author(self):
        return 'vla6' # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values

        See https://www.youtube.com/watch?v=WVc3cjvDHhw for more information on building the tree
        """
        indices = np.random.choice(dataX.shape[0], size=dataX.shape[0])
        for learner in self.learners:
            learner.addEvidence(dataX[indices], dataY[indices])

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        queries = ()
        for learner in self.learners:
            queries = queries + ([learner.query(points)], )
        results = np.concatenate(queries, axis=0)
        testY = np.mean(results, axis=0)
        return testY


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
