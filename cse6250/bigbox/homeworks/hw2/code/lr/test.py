#!/usr/bin/env python

"""
This file should test the model you develop in LogisticRegressionSGD,
it should not be changed
"""

import sys
import pickle
from optparse import OptionParser

from sklearn.metrics import roc_curve, auc
from sklearn.datasets import load_svmlight_file

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from lrsgd import LogisticRegressionSGD
from utils import parse_svm_light_data

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-m", "--model-path", action="store", dest="path",
                      default="model.txt", help="path where trained classifier was saved")
    parser.add_option("-r", "--result", action="store", dest="result",
                      default="roc", help="path of the saved roc figure, make sure the folder exists")

    options, args = parser.parse_args(sys.argv)

    with open(options.path, 'rb') as f:
        classifier = pickle.load(f)
        y_test_prob = []
        y_test = []
        for X, y in parse_svm_light_data(sys.stdin):
            y_prob = classifier.predict_prob(X)
            y_test.append(y)
            y_test_prob.append(y_prob)

        fpr, tpr, _ = roc_curve(y_test, y_test_prob)
        roc_auc = auc(fpr, tpr)

        # Plot of a ROC curve for a specific class
        plt.figure()
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        plt.savefig(options.result)
