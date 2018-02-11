"""
Test a learner.  (c) 2015 Tucker Balch

Run Command:
python testlearner.py Data/Istanbul_test.csv
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import LinRegLearner as lrl
import DTLearner as dt
import BagLearner as bl
import RTLearner as rt
import sys

if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)
    inf = open(sys.argv[1])
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    # compute how much of the data is training and testing
    train_rows = int(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]

    print testX.shape
    print testY.shape

    # create a learner and train it
    learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner
    learner.addEvidence(trainX, trainY) # train it
    print learner.author()

    # evaluate in sample
    predY = learner.query(trainX) # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    # evaluate out of sample
    predY = learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]

    # Testing DT Learner
    data_lecture = np.array([
        [0.61, 0.63, 8.4, 3],
        [0.885, 0.33, 9.1, 4],
        [0.56, 0.5, 9.4, 6],
        [0.735, 0.57, 9.8, 5],
        [0.32, 0.78, 10, 6],
        [0.26, 0.63, 11.8, 8],
        [0.5, 0.68, 10.5, 7],
        [0.725, 0.39, 10.9, 5],
    ])
    trainX_lecture = data_lecture[:, 0:-1]
    trainY_lecture = data_lecture[:, -1]

    learner = dt.DTLearner(leaf_size = 1, verbose = False) # constructor
    learner.author()

    learner.addEvidence(trainX_lecture, trainY_lecture) # training step
    print('learner tree')
    print(learner.tree)

    textX_lecture = np.array([
        [0.5, 0.7, 9.0],
        [0.33, 0.8, 10],
    ])
    print('testing query')
    Y = learner.query(textX_lecture) # query
    print(Y)

    # Answering Report Question 1
    # Does overfitting occur with respect to leaf size?

    print('Starting to Answer Report Question 1')

    # create a learner and train it

    def test_dt_learner(leaf_size):
        learner = dt.DTLearner(leaf_size=leaf_size, verbose = True)
        learner.addEvidence(trainX, trainY) # train it

        # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        train_rmse = rmse

        c = np.corrcoef(predY, y=trainY)
        train_corr = c[0, 1]

        # evaluate out of sample
        predY = learner.query(testX) # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        test_rmse = rmse

        c = np.corrcoef(predY, y=testY)
        test_corr = c[0, 1]

        return train_rmse, train_corr, test_rmse, test_corr


    def test_rt_learner(leaf_size):
        learner = rt.RTLearner(leaf_size=leaf_size, verbose = True)
        learner.addEvidence(trainX, trainY) # train it

        # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        train_rmse = rmse

        c = np.corrcoef(predY, y=trainY)
        train_corr = c[0, 1]

        # evaluate out of sample
        predY = learner.query(testX) # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        test_rmse = rmse

        c = np.corrcoef(predY, y=testY)
        test_corr = c[0, 1]

        return train_rmse, train_corr, test_rmse, test_corr


    max_leaf_size = 300
    train_rmses = np.array([])
    train_corrs = np.array([])
    test_rmses = np.array([])
    test_corrs = np.array([])
    for l in range(1, max_leaf_size):
        train_rmse, train_corr, test_rmse, test_corr = test_dt_learner(l)
        train_rmses = np.append(train_rmses, train_rmse)
        train_corrs = np.append(train_corrs, train_corr)
        test_rmses = np.append(test_rmses, test_rmse)
        test_corrs = np.append(test_corrs, test_corr)
    df = pd.DataFrame({
        'leaf_size': list(range(1, max_leaf_size)),
        'bags': [0] * len(list(range(1, max_leaf_size))),
        'train_rmse': train_rmses,
        'train_corr': train_corrs,
        'test_rmse': test_rmses,
        'test_corr': test_corrs
    })
    print(df.head())
    df.to_csv('question1.csv')

    plt.figure(figsize=(7, 4))
    plt.plot(df['train_rmse'], color='b', label='Train RMSE')
    plt.plot(df['test_rmse'], color='g', label='Test RMSE')
    plt.grid(True)
    plt.legend(loc=0)
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('Test vs Train RMSE')
    plt.show()
    plt.savefig('./plot.png')

    # Answering Report Question 2
    # Can bagging reduce or eliminate overfitting with respect to leaf size?

    print('Starting to Answer Report Question 2')

    def test_bag_learner(learner, bags, leaf_size):
        learner = bl.BagLearner(learner=learner, kwargs={'leaf_size': leaf_size}, bags=bags, boost=False, verbose=True)
        learner.addEvidence(trainX, trainY) # train it

        # evaluate in sample
        predY = learner.query(trainX) # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        train_rmse = rmse

        c = np.corrcoef(predY, y=trainY)
        train_corr = c[0, 1]

        # evaluate out of sample
        predY = learner.query(testX) # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        test_rmse = rmse

        c = np.corrcoef(predY, y=testY)
        test_corr = c[0, 1]

        return train_rmse, train_corr, test_rmse, test_corr

    bags = np.array([1, 15, 30, 200])
    leaf_sizes = list(range(1, 50))  # + list(range(51, 150, 5)) + list(range(151, 300, 10))
    bags_total = bags.repeat(len(leaf_sizes))
    leaf_sizes_total = np.tile(leaf_sizes, len(bags))

    dfdt = pd.DataFrame({
        'leaf_size': leaf_sizes_total,
        'bags': bags_total,
    })

    train_rmses = np.array([])
    train_corrs = np.array([])
    test_rmses = np.array([])
    test_corrs = np.array([])
    for index, row in dfdt.iterrows():
        l = row['leaf_size']
        b = row['bags']

        train_rmse, train_corr, test_rmse, test_corr = test_bag_learner(learner=dt.DTLearner, bags=b, leaf_size=l)
        train_rmses = np.append(train_rmses, train_rmse)
        train_corrs = np.append(train_corrs, train_corr)
        test_rmses = np.append(test_rmses, test_rmse)
        test_corrs = np.append(test_corrs, test_corr)
    dfdt['train_rmse'] = train_rmses
    dfdt['train_corr'] = train_corrs
    dfdt['test_rmse'] = test_rmses
    dfdt['test_corr'] = test_corrs
    print(dfdt.head())
    dfdt.to_csv('question2.csv')

    dfdt_combined = pd.concat([df.loc[df.leaf_size <= 10], dfdt.loc[dfdt.leaf_size <= 10]])
    dfdt_combined_large = pd.concat([df.loc[df.leaf_size <= 50], dfdt.loc[dfdt.leaf_size <= 50]])

    dfdt1 = dfdt_combined.loc[dfdt_combined.bags==0]
    dfdt10 = dfdt_combined.loc[dfdt_combined.bags==15]
    dfdt200 = dfdt_combined.loc[dfdt_combined.bags==200]
    dfdtlarge1 = dfdt_combined_large.loc[dfdt_combined_large.bags==0]
    dfdtlarge10 = dfdt_combined_large.loc[dfdt_combined_large.bags==15]
    dfdtlarge200 = dfdt_combined_large.loc[dfdt_combined_large.bags==200]

    dfdt1.set_index('leaf_size', inplace=True)
    dfdt10.set_index('leaf_size', inplace=True)
    dfdt200.set_index('leaf_size', inplace=True)
    dfdtlarge1.set_index('leaf_size', inplace=True)
    dfdtlarge10.set_index('leaf_size', inplace=True)
    dfdtlarge200.set_index('leaf_size', inplace=True)

    plt.figure(figsize=(7, 4))
    plt.plot(dfdt1['test_rmse'], linestyle='dashed', color='g', label='Test RMSE (No Bagging)')
    plt.plot(dfdt10['test_rmse'], color='g', label='Test RMSE (Bags = 15)')
    plt.plot(dfdt200['test_rmse'], color='c', label='Test RMSE (Bags = 200)')
    plt.grid(True)
    plt.legend(loc=0)
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('Test vs Train RMSE')
    plt.show()
    plt.savefig('./plot2.png')

    plt.figure(figsize=(7, 4))
    plt.plot(dfdtlarge1['test_rmse'], linestyle='dashed', color='g', label='Test RMSE (No Bagging)')
    plt.plot(dfdtlarge10['test_rmse'], color='g', label='Test RMSE (Bags = 15)')
    plt.plot(dfdtlarge200['test_rmse'], color='c', label='Test RMSE (Bags = 200)')
    plt.grid(True)
    plt.legend(loc=0)
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('Test RMSE')
    plt.show()
    plt.savefig('./plot2b.png')

    # Answering Report Question 3
    # Quantiatively Compare DT learner vs RT learner. In which Ways is one method better than the other?

    print('Starting to Answer Report Question 3')

    # No Bagging Random Tree:
    train_rmses = np.array([])
    train_corrs = np.array([])
    test_rmses = np.array([])
    test_corrs = np.array([])
    for l in range(1, max_leaf_size):
        train_rmse, train_corr, test_rmse, test_corr = test_rt_learner(l)
        train_rmses = np.append(train_rmses, train_rmse)
        train_corrs = np.append(train_corrs, train_corr)
        test_rmses = np.append(test_rmses, test_rmse)
        test_corrs = np.append(test_corrs, test_corr)
    dfrt_nobagging = pd.DataFrame({
        'leaf_size': list(range(1, max_leaf_size)),
        'bags': [0] * len(list(range(1, max_leaf_size))),
        'train_rmse': train_rmses,
        'train_corr': train_corrs,
        'test_rmse': test_rmses,
        'test_corr': test_corrs
    })

    dfrt = pd.DataFrame({
        'leaf_size': leaf_sizes_total,
        'bags': bags_total,
    })

    train_rmses = np.array([])
    train_corrs = np.array([])
    test_rmses = np.array([])
    test_corrs = np.array([])
    for index, row in dfrt.iterrows():
        l = row['leaf_size']
        b = row['bags']

        train_rmse, train_corr, test_rmse, test_corr = test_bag_learner(learner=rt.RTLearner, bags=b, leaf_size=l)
        train_rmses = np.append(train_rmses, train_rmse)
        train_corrs = np.append(train_corrs, train_corr)
        test_rmses = np.append(test_rmses, test_rmse)
        test_corrs = np.append(test_corrs, test_corr)
    dfrt['train_rmse'] = train_rmses
    dfrt['train_corr'] = train_corrs
    dfrt['test_rmse'] = test_rmses
    dfrt['test_corr'] = test_corrs
    print(dfrt.head())

    dfdt_combined['learner'] = 'DTLearner'
    dfrt['learner'] = 'RTLearner'

    dfdtrt_combined = pd.concat([dfdt_combined, dfrt_nobagging, dfrt])
    dfdtrt_combined.to_csv('question3.csv')

    dfrt1 = dfrt_nobagging.loc[(dfrt_nobagging.bags==0) & (dfrt_nobagging.leaf_size <= 50)]
    dfrt10 = dfrt.loc[(dfrt.bags==15) & (dfrt.leaf_size <= 50)]
    dfrt20 = dfrt.loc[(dfrt.bags==30) & (dfrt.leaf_size <= 50)]
    dfrt200 = dfrt.loc[(dfrt.bags==200) & (dfrt.leaf_size <= 50)]

    dfrt1.set_index('leaf_size', inplace=True)
    dfrt10.set_index('leaf_size', inplace=True)
    dfrt20.set_index('leaf_size', inplace=True)
    dfrt200.set_index('leaf_size', inplace=True)

    plt.figure(figsize=(7, 4))
    plt.plot(dfdtlarge200['test_rmse'], color='r', label='Test RMSE (DTLearner Bags = 200)')
    plt.plot(dfrt200['test_rmse'], color='c', label='Test RMSE (RTLearner Bags = 200)')
    plt.grid(True)
    plt.legend(loc=0)
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('Test RMSE (DT vs RT Learner Comparison with Bagging)')
    plt.show()
    plt.savefig('./plot3.png')

    plt.figure(figsize=(7, 4))
    plt.plot(dfdtlarge1['test_rmse'], color='r', label='Test RMSE (DTLearner No Bagging)')
    plt.plot(dfrt1['test_rmse'], color='c', label='Test RMSE (RTLearner No Bagging)')  # This produces no graph because RT with one leaf fails
    plt.grid(True)
    plt.legend(loc=0)
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('Test vs Train RMSE')
    plt.show()
    plt.savefig('./plot3b.png')
