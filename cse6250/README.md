# CSE 6250: Big Data for Healthcare

Course Link: http://www.sunlab.org/teaching/cse6250/fall2018/schedule.html
Piazza: https://piazza.com/class/jjjilbkqk8m1r4?cid=8

## Useful Links for HW2

https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/pdfs/40%20LogisticRegression.pdf
http://www.cs.cmu.edu/~wcohen/10-605/sgd-part2.pdf

## Useful Links for Project
https://github.com/bryantravissmith/In-Hospital-Mortality-Predictions-With-Scala-on-MIMIC-III/blob/master/paper/mortality_predictions.pdf

## Useful Commands
Runs a docker container with options represent in a YAML config
```
docker-compose up
```

SSH into Docker Container
```
ssh -p 2333 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ./config/ssh/id_rsa root@127.0.0.1
```

Start the HIVE Server for Python
```
hive --service hiveserver2 --hiveconf hive.server2.thrift.port=10000 --hiveconf hive.root.logger=INFO,console --hiveconf hive.server2.authentication=NOSASL
```

Tar directory
```
tar -czvf 903178639-vla6-hw4.tar.gz 903178639-vla6-hw4
```
