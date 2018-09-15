# BigBox

Yet another integrated envoronment.

Please refere to <http://sunlab.org/teaching/cse6250/fall2018/env/env-local-docker.html> for detail instruction.

```
docker run -it -m 8192m -h bootcamp.local \
  --name bigbox -p 2222:22 -p 9530:9530 -p 8888:8888\
  sunlab/bigbox:latest \
  /bin/bash
```

Related Links:

+ Docker Image: [https://hub.docker.com/r/sunlab/bigbox/](https://hub.docker.com/r/sunlab/bigbox/)
+ FAQs: [https://github.com/yuikns/bigbox/wiki/FAQ](https://github.com/yuikns/bigbox/wiki/FAQ)
+ Sample Code: [https://bitbucket.org/realsunlab/bigdata-bootcamp](https://bitbucket.org/realsunlab/bigdata-bootcamp)
+ Scripts: [https://github.com/yuikns/bigbox-scripts](https://github.com/yuikns/bigbox-scripts)



