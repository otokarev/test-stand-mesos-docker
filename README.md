MESOS
-----

```
for i in `sudo docker -H 192.168.2.2:4000 ps -a --format "{{.Image}} {{.Names}}" | grep elastic | gawk '{print $2}'`; do sudo docker -H 192.168.2.2:4000 stop $i; sudo docker -H 192.168.2.2:4000 rm $i; done

sudo docker -H 192.168.2.2:4000 ps -a

sudo docker -H 192.168.2.2:4000 network create --driver overlay --subnet=10.0.9.0/24 es-net

sudo docker run --net host --name hui --rm -i -t ubuntu /bin/bash

# Create elasticsearch cluster
curl -k -XPUT -d @playbooks/mesos-cluster/es.json -H "Content-Type: application/json" http://master2.mesos.boom:8080/v2/apps

# Clean up known_hosts after vpses recreation
for i in 2 3 4 5 6 7; do ssh-keygen -f "/home/otokarev/.ssh/known_hosts" -R 192.168.2.$i; done
```



SPARK
-----
First of all we need mesos shared library /usr/local/lib/libmesos.so (installed by default on all masters and nodes)


Seems the way below takes too much time for tgz download and gives up finally

```

   export \
       SPARK_EXECUTOR_URI=http://apache-mirror.rbc.ru/pub/apache/spark/spark-1.6.1/spark-1.6.1-bin-hadoop2.6.tgz \
       MESOS_NATIVE_JAVA_LIBRARY=/usr/local/lib/libmesos.so
   
   /tmp/spark-1.6.1-bin-hadoop2.6/bin/spark-shell \
       --master mesos://zk://192.168.2.2:2181/mesos \
       --num-executors 2 \
       --executor-cores 0.2 \
       --executor-memory 512M
   
```

The way with executor's home works better (somehow it does not work from host system but it works from other vbox VPS):

```
export MESOS_NATIVE_JAVA_LIBRARY=/usr/local/lib/libmesos.so
/tmp/spark-1.6.1-bin-hadoop2.6/bin/spark-shell --master mesos://zk://192.168.2.2:2181/mesos --num-executors 3 --executor-cores 1 --executor-memory 512M -c spark.mesos.executor.home=/tmp/spark-1.6.1-bin-hadoop2.6/
```

Test for spark-shell:

```
sc.parallelize((1 to 1000)).foreach((x) => Thread.sleep(1000))
```

Take care about --executor-memory, executor will not start if a node has no enough memory

Before that we should install java-1.8 on all nodes, and upload spark

Mesos-DNS
---------

Install external role:

```
ansible-galaxy install tumf.systemd-service
```

Check that Mesos DNS works

```
dig @192.168.2.2 _elasticsearch-executor._tcp.elasticsearch.mesos.boom SRV
dig @192.168.2.2 _elasticsearch._tcp.marathon.mesos.boom SRV
```

Consul UI
---------

```
http://192.168.2.2:8500
```

Deploy Mesos-Consul by Marathon

```
curl -k -XPUT -d @./roles/mesos/consul/templates/mesos-consul.json -H "Content-Type: application/json" http://master2.mesos.boom:8080/v2/apps
```

```
dig @192.168.2.2 -p 8600 master2.mesos.boom.node.consul
dig @192.168.2.2 -p 8600 nodes.consul
dig @192.168.2.2 -p 8600 elasticsearch.nodes.consul
dig @192.168.2.2 -p 8600 mesos.nodes.consul
dig @192.168.2.2 -p 8600 mesos.service.consul
dig @192.168.2.2 -p 8600 consul.service.consul
dig @192.168.2.2 -p 8600 mesos.service.consul
dig @192.168.2.2 -p 8600 elasticsearch.service.consul
dig @192.168.2.2 -p 8600 elasticsearch-executor.service.consul
dig @192.168.2.2 -p 8600 elasticsearch-executor.service.consul SRV
dig @192.168.2.2 -p 8600 elasticsearch-executor.service.consul ANY
dig @192.168.2.2 -p 8600 CLIENT_PORT.elasticsearch-executor.service.consul ANY
dig @192.168.2.2 -p 8600 _elasticsearch-executor._CLIENT_PORT.service.consul ANY
dig @192.168.2.2 -p 8600 _elasticsearch-executor._CLIENT_PORT.service.consul SRV
dig @192.168.2.2 -p 8600 _elasticsearch-executor._TRANSPORT_PORT.service.consul SRV
```

Docker
------

You can try to resolve:

```
Error initializing network controller: Error creating default \"bridge\" network: failed to allocate gateway (172.17.0.1): Address already in use
```

By:

```
sudo rm -rf /var/lib/docker/network/files/
```
