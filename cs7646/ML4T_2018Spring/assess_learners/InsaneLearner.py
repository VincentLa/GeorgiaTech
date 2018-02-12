import numpy as np
import BagLearner as bl
import LinRegLearner as lrl

class InsaneLearner(object):

    def __init__(self, verbose=False):
        self.learner = bl.BagLearner(bl.BagLearner, {'learner':lrl.LinRegLearner, 'kwargs':{}, 'bags':20}, bags = 20)

    def author(self):
        return 'vla6' # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        self.learner.addEvidence(dataX, dataY)

    def query(self, points):
        return self.learner.query(points)

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
