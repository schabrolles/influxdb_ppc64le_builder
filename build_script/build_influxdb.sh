#!/bin/sh
#
# s.chabrolles@fr.ibm.com
#########################

if [ $# -ne 2 ] ; then
	echo "Need 2 parameters: <build type> <branch name>"
	echo "build type in : packages, static, all"
	exit 1
fi

build_type=$1
branch=$2

case $build_type in
	all)
		build_packages=1
		build_static=1
	;;

	static)
		build_packages=0
		build_static=1
	;;

	packages)
		build_packages=1
		build_static=0
	;;

	*)
		echo "Bad build type specified:"
		echo "build type must be in : packages, static, all"
		exit 1
esac

export DEBIAN_FRONTEND=noninteractive

apt-get update && apt-get -y upgrade

apt-get install -y git golang ruby ruby-dev libffi-dev rpm

gem install fpm

export GOPATH=/go
export GIT_REPO_NAME=schabrolles
mkdir -p $GOPATH/src/github.com/influxdata/influxdb
git clone https://gitlab.com/$GIT_REPO_NAME/influxdb.git $GOPATH/src/github.com/influxdata/influxdb -b $branch
cd $GOPATH/src/github.com/influxdata/influxdb

if [ $build_packages -eq 1 ]; then
	python3 ./build.py --package --release
fi

if [ $build_static -eq 1 ]; then
	python3 ./build.py --static
fi

cp -rp $GOPATH/src/github.com/influxdata/influxdb/build/* /build_output
