#!/usr/bin/env python

import sys
import os
import pickle

from optparse import OptionParser

from sklearn.metrics import roc_curve, auc
from sklearn.datasets import load_svmlight_file

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from lrsgd import LogisticRegressionSGD
from utils import parse_svm_light_data


def load_model(path):
    with open(path, 'rb') as f:
        content_list = [x.replace(b'\t\n', b'\n') for x in f.readlines()]
    with open('pickled.txt', 'wb') as ufile:
        for line in content_list:
            ufile.write(line)
    with open('pickled.txt', 'rb') as ifile:
        classifier = pickle.load(ifile)
    return classifier

def predict_prob(classifiers, X):
    """
    Given a list of trained classifiers,
    predict the probability of positive label.
    (Return the average obtained from all the classifiers)
    """
    pass


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-m", "--model-path", action="store", dest="path",
                      default="models", help="path where trained classifiers are saved")
    parser.add_option("-r", "--result", action="store", dest="result",
                      default="roc", help="name of the figure")
    
    options, args = parser.parse_args(sys.argv)

    files = [options.path + "/" +
             filename for filename in os.listdir(options.path) if filename.startswith('part')]
    classifiers = list(map(load_model, files))
    y_test_prob = []
    y_test = []
    for X, y in parse_svm_light_data(sys.stdin):
        y_prob = predict_prob(classifiers, X)
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
