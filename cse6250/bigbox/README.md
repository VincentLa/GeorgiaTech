# BigBox

Yet another integrated envoronment.

Please refere to <http://sunlab.org/teaching/cse6250/fall2018/env/env-local-docker.html> for detail instruction.

```
docker run -it -m 8192m -h bootcamp.local \
  --name bigbox -p 2222:22 -p 9530:9530 -p 8888:8888\
  sunlab/bigbox:latest \
  /bin/bash
```

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


Related Links:

+ Docker Image: [https://hub.docker.com/r/sunlab/bigbox/](https://hub.docker.com/r/sunlab/bigbox/)
+ FAQs: [https://github.com/yuikns/bigbox/wiki/FAQ](https://github.com/yuikns/bigbox/wiki/FAQ)
+ Sample Code: [https://bitbucket.org/realsunlab/bigdata-bootcamp](https://bitbucket.org/realsunlab/bigdata-bootcamp)
+ Scripts: [https://github.com/yuikns/bigbox-scripts](https://github.com/yuikns/bigbox-scripts)



