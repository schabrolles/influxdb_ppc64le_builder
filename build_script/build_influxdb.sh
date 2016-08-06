#!/bin/sh
#
# s.chabrolles@fr.ibm.com
#########################

if [ -z $1 ] ; then
	branch="stable"
else
	branch=$1
fi 

export DEBIAN_FRONTEND=noninteractive

apt-get update && apt-get -y upgrade

apt-get install -y git golang ruby ruby-dev libffi-dev rpm

gem install fpm

export GOPATH=/go
export GITHUB_REPO=schabrolles
mkdir -p $GOPATH/src/github.com/influxdata/influxdb
git clone https://github.com/$GITHUB_REPO/influxdb.git $GOPATH/src/github.com/influxdata/influxdb -b $branch
cd $GOPATH/src/github.com/influxdata/influxdb

python3 ./build.py --static
#python3 ./build.py --static --package --release
#python3 ./build.py --package --release

cp -rp $GOPATH/src/github.com/influxdata/influxdb/build/* /build_output

