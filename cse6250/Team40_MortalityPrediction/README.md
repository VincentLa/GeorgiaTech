# Georgia Tech CSE6250 Big Data for Healthcare Project
Authors:
1. Avi Ananthakrishnan
2. Vincent La

All relevant code is located inside the [project](./project) directory. This top level directory contains the Dockerfile and docker-compose.yml file to create the Docker Container.

However, to see the actual code go into the [project](./project) directory. In particular, the [project/README.md](./project/README.md) file will contain instructions on how to actually run the code.

## Useful Commands
Runs a docker container with options represent in a YAML config
```
docker-compose up
```

SSH into Docker Container
```
ssh -p 2333 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ./config/ssh/id_rsa root@127.0.0.1
```

Start Hive Service
```
sudo service hive-service start
```

Start the HIVE Server for Python
```
hive --service hiveserver2 --hiveconf hive.server2.thrift.port=10000 --hiveconf hive.root.logger=INFO,console --hiveconf hive.server2.authentication=NOSASL
```


Related Links:

+ Docker Image: [https://hub.docker.com/r/sunlab/bigbox/](https://hub.docker.com/r/sunlab/bigbox/)
+ FAQs: [https://github.com/yuikns/bigbox/wiki/FAQ](https://github.com/yuikns/bigbox/wiki/FAQ)
+ Sample Code: [https://bitbucket.org/realsunlab/bigdata-bootcamp](https://bitbucket.org/realsunlab/bigdata-bootcamp)
+ Scripts: [https://github.com/yuikns/bigbox-scripts](https://github.com/yuikns/bigbox-scripts)



