MESOS
-----
for i in `sudo docker -H 192.168.2.2:4000 ps -a --format "{{.Image}} {{.Names}}" | grep elastic | gawk '{print $2}'`; do sudo docker -H 192.168.2.2:4000 stop $i; sudo docker -H 192.168.2.2:4000 rm $i; done

sudo docker -H 192.168.2.2:4000 ps -a

sudo docker -H 192.168.2.2:4000 network create --driver overlay --subnet=10.0.9.0/24 es-net

sudo docker run --net host --name hui --rm -i -t ubuntu /bin/bash

curl -k -XPOST -d @es.json -H "Content-Type: application/json" http://master2.mesos.boom:8080/v2/apps

TODO:

посмотреть в кого резолвится в контейнере хостнейм пира, похоже, что в 10ую сетку

for i in 2 3 4 5 6 7; do ssh-keygen -f "/home/otokarev/.ssh/known_hosts" -R 192.168.2.$i; done

SPARK
-----
First of all we need mesos shared library /usr/local/lib/libmesos.so (installed by default on all masters and nodes)


Seems the way below takes too much time for tgz download and gives up finally

```
export SPARK_EXECUTOR_URI=http://apache-mirror.rbc.ru/pub/apache/spark/spark-1.6.1/spark-1.6.1-bin-hadoop2.6.tgz MESOS_NATIVE_JAVA_LIBRARY=/usr/local/lib/libmesos.so
/tmp/spark-1.6.1-bin-hadoop2.6/bin/spark-shell --master mesos://zk://192.168.2.2:2181/mesos --num-executors 3 --executor-cores 1 --executor-memory 512M
```

The way with executor's home works better (somehow it does not work from host system but it works from other vbox VPS):

```
export MESOS_NATIVE_JAVA_LIBRARY=/usr/local/lib/libmesos.so
/tmp/spark-1.6.1-bin-hadoop2.6/bin/spark-shell --master mesos://zk://192.168.2.2:2181/mesos --num-executors 3 --executor-cores 1 --executor-memory 512M -c spark.mesos.executor.home=/tmp/spark-1.6.1-bin-hadoop2.6/
```

Test for spark-shell:
```
val data = Array(range(1,1000))
sc.parallelize(data).foreach((x) => Thread.sleep(1000))
```

Take care about --executor-memory, executor will not start if a node has no enough memory

Before that we should install java-1.8 on all nodes, and upload spark

