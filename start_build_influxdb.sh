#!/bin/sh
#
# s.chabrolles@fr.ibm.com
#########################

mkdir -p build_output

#docker run --rm -ti -v $PWD/opt:/opt -v $PWD/build_script:/build_script --name grafana2_build schabrolles/ubuntu_ppc64le:15.04 /build_script/build_grafana2.sh
docker run --rm -ti -v $PWD/build_output:/build_output -v $PWD/build_script:/build_script --name influxdb_build docker.io/schabrolles/ubuntu_ppc64le:16.04 /build_script/build_influxdb.sh $1

rm -f build_docker/*.tar.gz
cd build_output
tar zcvf ../build_docker/influxdb-static_ppc64le.tar.gz .

cd ../build_docker/
docker build -t docker.io/schabrolles/influxdb_ppc64le .

