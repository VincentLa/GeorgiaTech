#!/usr/bin/env bash

source /etc/profile
source /etc/bashrc

### INIT
# sudo service zookeeper-server start
# sudo service hadoop-yarn-proxyserver start
# sudo service hadoop-yarn-resourcemanager start
# sudo service hadoop-yarn-nodemanager start
# sudo service hadoop-hdfs-namenode start
# sudo service hadoop-hdfs-datanode start
#
# sudo -u hdfs hdfs dfs -mkdir -p /app
# sudo -u hdfs hdfs dfs -chmod 777 /app
# sudo -u hdfs hdfs dfs -mkdir -p /user
# sudo -u hdfs hdfs dfs -chmod 755 /user
#
# # for hive
# sudo -u hdfs hdfs dfs -mkdir -p /user/hive/warehouse
# sudo -u hdfs hdfs dfs -chown -R root /user/hive
# # for hive and hadoop-mapreduce-historyserver and so on
# sudo -u hdfs hdfs dfs -mkdir -p /tmp
# sudo -u hdfs hdfs dfs -chmod 777 /tmp
#
# # for user
# sudo -u hdfs hdfs dfs -mkdir -p /user/root
# sudo -u hdfs hdfs dfs -chown -R root /user/root
#
# sudo service hadoop-mapreduce-historyserver start
#
# sudo service spark-worker start
# sudo service spark-master start
#
# sudo service hbase-regionserver start
# sudo service hbase-master start
# sudo service hbase-thrift start

sudo chmod 0777  /var/log
sudo mkdir -p /var/log/spark
sudo chmod 0777 /var/log/spark
sudo mkdir -p /tmp/spark-events
sudo chmod 0777 /tmp/spark-events


sudo service zookeeper-server start
sudo service hadoop-yarn-proxyserver start
sudo service hadoop-yarn-resourcemanager start
sudo service hadoop-yarn-nodemanager start
sudo service hadoop-hdfs-namenode start
sudo service hadoop-hdfs-datanode start

sudo service hadoop-mapreduce-historyserver start

sudo service spark-worker start
sudo service spark-master start

sudo service hbase-regionserver start
sudo service hbase-master start
sudo service hbase-thrift start


echo "master is ready, rock it!"
# Holding over here
/usr/sbin/sshd -D

