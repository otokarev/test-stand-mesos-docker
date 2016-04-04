for i in `sudo docker -H 192.168.2.2:4000 ps -a --format "{{.Image}} {{.Names}}" | grep elastic | gawk '{print $2}'`; do sudo docker -H 192.168.2.2:4000 stop $i; sudo docker -H 192.168.2.2:4000 rm $i; done

sudo docker -H 192.168.2.2:4000 ps -a

sudo docker -H 192.168.2.2:4000 network create --driver overlay --subnet=10.0.9.0/24 es-net

sudo docker run --net host --name hui --rm -i -t ubuntu /bin/bash

curl -k -XPOST -d @es.json -H "Content-Type: application/json" http://master2.mesos.boom:8080/v2/apps

TODO:

посмотреть в кого резолвится в контейнере хостнейм пира, похоже, что в 10ую сетку

for i in 2 3 4 5 6 7; do ssh-keygen -f "/home/otokarev/.ssh/known_hosts" -R 192.168.2.$i; done
