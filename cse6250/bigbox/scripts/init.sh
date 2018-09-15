#!/usr/bin/env bash

[ ! -f /etc/profile.d/bigbox.sh ] && touch /etc/profile.d/bigbox.sh

source /etc/profile.d/bigbox.sh
source /etc/bashrc

cat >> /etc/profile.d/bigbox.sh <<'EOF'
# Hadoop Base
export ZOOKEEPER_HOME=/usr/lib/zookeeper
export ZOOKEEPER_CONF_DIR=/etc/zookeeper/conf

export HADOOP_HOME=/usr/lib/hadoop
export HADOOP_CONF_DIR=/etc/hadoop/conf
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
# ?
# export YARN_HOME=$HADOOP_HOME
# export YARN_CONF_DIR=$HADOOP_CONF_DIR
export SPARK_HOME=/usr/lib/spark
export HBASE_HOME=/usr/lib/hbase
export HIVE_HOME=/usr/lib/hive
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_HOME/lib/native"
# WHY DOES NOT WORK?
# export HADOOP_CLASSPATH="$HADOOP_CLASSPATH:$HIVE_HOME/lib/*"
# Zeppelin Section
unset ZEPPELIN_MEM
unset ZEPPELIN_INTP_MEM
# export ZEPPELIN_MEM=" -Xms2048m -Xmx2048m -XX:MaxPermSize=1024m "
# export ZEPPELIN_INTP_MEM=" -Xms1024m -Xmx2048m -XX:MaxPermSize=1024m "
export ZEPPELIN_INTP_MEM=" -Xms512m -Xmx2048m "
# Collect All
export PIG_CLASSPATH=$PIG_CLASSPATH:$HADOOP_CONF_DIR:$HADOOP_CLASSPATH
export CLASSPATH=$CLASSPATH:$HADOOP_CONF_DIR


export PATH=$PATH:$ZOOKEEPER_HOME/bin

EOF

echo '127.0.0.1 bootcamp.local' >> /etc/hosts

source /etc/profile.d/bigbox.sh

# Fix: Class org.datanucleus.api.jdo.JDOPersistenceManagerFactory was not found.
#
# for spark 1.5
# ln -sf /usr/lib/hive/lib/datanucleus-* /usr/lib/spark/lib/
# for spark 2.0
ln -sf /usr/lib/hive/lib/datanucleus-* /usr/lib/spark/jars/

# for mysql in hive
## mv /etc/hive/conf/mysql* /usr/lib/hive/lib/ # NOT required even for mysql
# ln -s /usr/share/java/mysql-connector-java.jar $HIVE_HOME/lib/mysql-connector-java.jar


# http://central.maven.org/maven2/org/apache/derby/derbyclient/10.14.1.0/derbyclient-10.14.1.0.jar

# Fix: Failed In Stop Services
# patch -fs /etc/init.d/hadoop-hdfs-namenode /scripts/patch/hadoop-hdfs-namenode.patch
# patch -fs /etc/init.d/hadoop-hdfs-datanode /scripts/patch/hadoop-hdfs-datanode.patch

# Zeppelin is another super user
echo 'zeppelin ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/zeppelin

mkdir -p /data
chown -R hdfs:hadoop /data

# service init
sudo -u root service hadoop-hdfs-namenode init
sudo -u root service zookeeper-server condrestart

# Spark Log
sudo mkdir -p /var/log/spark/
sudo mkdir -p /tmp/spark-events
sudo chmod 0777 /tmp/spark-events


sudo service zookeeper-server start
sudo service hadoop-yarn-proxyserver start
sudo service hadoop-yarn-resourcemanager start
sudo service hadoop-yarn-nodemanager start
sudo service hadoop-hdfs-namenode start
sudo service hadoop-hdfs-datanode start

sudo -u hdfs hdfs dfs -mkdir -p /app
sudo -u hdfs hdfs dfs -chmod 777 /app
sudo -u hdfs hdfs dfs -mkdir -p /user
sudo -u hdfs hdfs dfs -chmod 755 /user

# for hive
sudo -u hdfs hdfs dfs -mkdir -p /user/hive/warehouse
sudo -u hdfs hdfs dfs -chown -R root /user/hive
# for hive and hadoop-mapreduce-historyserver and so on
sudo -u hdfs hdfs dfs -mkdir -p /tmp
sudo -u hdfs hdfs dfs -chmod 777 /tmp
# for spark
sudo -u hdfs hdfs dfs -mkdir -p /tmp/spark-events
sudo -u hdfs hdfs dfs -chmod 777 /tmp/spark-events

# for user
sudo -u hdfs hdfs dfs -mkdir -p /user/root
sudo -u hdfs hdfs dfs -chown -R root /user/root

sudo service hadoop-yarn-nodemanager stop
sudo service hadoop-hdfs-datanode stop
sudo service hadoop-hdfs-namenode stop
sudo service hadoop-yarn-resourcemanager stop
sudo service hadoop-yarn-proxyserver stop
sudo service zookeeper-server stop

echo "done.."
