#!/usr/bin/env python

"""
Before you can run this need to run the following in terminal
1. sudo su - hdfs
2. hdfs dfs -mkdir -p /hw2
3. hdfs dfs -chown -R root /hw2
4. exit
5. hdfs dfs -put pig/training /hw2
   (Note that I am in the code directory when I do this)

To actually run do:
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -D mapreduce.job.reduces=5 -files lr -mapper "python lr/mapper.py -n 5 -r 0.4" -reducer "python lr/reducer.py -f 3618" -input /hw2/training -output /hw2/models

Also, before each next run, need to remove the output directory:
hadoop fs -rm -r /hw2/models
"""
import sys
import random

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-n", "--model-num", action="store", dest="n_model",
                  help="number of models to train", type="int")
parser.add_option("-r", "--sample-ratio", action="store", dest="ratio",
                  help="ratio to sample for each ensemble", type="float")

options, args = parser.parse_args(sys.argv)

random.seed(6505)

for line in sys.stdin:
    value = line.strip()
    for i in range(options.n_model):
        m = random.random()
        if m < options.ratio:
            print("{}\t{}".format(i, value))
