"""
QUESTION FOR JAMES
Not sure if this is implemented correctly. What does it mean contain 20 Bag Learner instances composed of 20 LinRegLearner instances?

Do I have to create 20 different BagLearner where in each the bags is equal to 20?
"""

import numpy as np
import pandas as pd

import BagLearner as bl
import LinRegLearner as lrl

class InsaneLearner(object):

    def __init__(self, verbose=False):
        self.learner = bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False)

    def author(self):
        return 'vla6' # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        self.learner.addEvidence(dataX, dataY)

    def query(self, points):
        testY = self.learner.query(points)
        return testY

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
