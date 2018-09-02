"""
Author: Vincent La
vla6

To test: nosetests tests/test_model_partb.py
"""

import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import *

import utils

# setup the randoms tate
RANDOM_STATE = 545510477

#input: X_train, Y_train
#output: Y_pred
def logistic_regression_pred(X_train, Y_train):
	#train a logistic regression classifier using X_train and Y_train. Use this to predict labels of X_train
	#use default params for the classifier

	logreg = LogisticRegression(random_state=RANDOM_STATE)
	logreg.fit(X_train, Y_train)
	y_pred = logreg.predict(X_train)
	return y_pred

#input: X_train, Y_train
#output: Y_pred
def svm_pred(X_train, Y_train):
	#train a SVM classifier using X_train and Y_train. Use this to predict labels of X_train
	#use default params for the classifier
	svm = LinearSVC(random_state=RANDOM_STATE)
	svm.fit(X_train, Y_train)
	y_pred = svm.predict(X_train)
	return y_pred

#input: X_train, Y_train
#output: Y_pred
def decisionTree_pred(X_train, Y_train):
	#train a logistic regression classifier using X_train and Y_train. Use this to predict labels of X_train
	#use max_depth as 5
	tree = DecisionTreeClassifier(random_state=RANDOM_STATE, max_depth=5)
	tree.fit(X_train, Y_train)
	y_pred = tree.predict(X_train)
	return y_pred

#input: Y_pred,Y_true
#output: accuracy, auc, precision, recall, f1-score
def classification_metrics(Y_pred, Y_true):
	#NOTE: It is important to provide the output in the same order
	accuracy = accuracy_score(y_true=Y_true, y_pred=Y_pred)
	area_under_curve = roc_auc_score(y_true=Y_true, y_score=Y_pred)
	precision = precision_score(y_true=Y_true, y_pred=Y_pred)
	recall = recall_score(y_true=Y_true, y_pred=Y_pred)
	f1score = f1_score(y_true=Y_true, y_pred=Y_pred)
	return accuracy, area_under_curve, precision, recall, f1score

#input: Name of classifier, predicted labels, actual labels
def display_metrics(classifierName,Y_pred,Y_true):
	print("______________________________________________")
	print(("Classifier: "+classifierName))
	acc, auc_, precision, recall, f1score = classification_metrics(Y_pred,Y_true)
	print(("Accuracy: "+str(acc)))
	print(("AUC: "+str(auc_)))
	print(("Precision: "+str(precision)))
	print(("Recall: "+str(recall)))
	print(("F1-score: "+str(f1score)))
	print("______________________________________________")
	print("")

def main():
	X_train, Y_train = utils.get_data_from_svmlight("../deliverables/features_svmlight.train")
	
	display_metrics("Logistic Regression",logistic_regression_pred(X_train,Y_train),Y_train)
	display_metrics("SVM",svm_pred(X_train,Y_train),Y_train)
	display_metrics("Decision Tree",decisionTree_pred(X_train,Y_train),Y_train)
	

if __name__ == "__main__":
	main()
	
