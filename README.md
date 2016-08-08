# influxdb_ppc64le_builder

**influxdb_ppc64le_builder** is a set of scripts (shell and python) to automate InfluxDB compilation and produce automatically binaries, packages docker images for POWER platform (ppc64le).

## Features
- Compilation made in a transient docker container (avoid local host pollution with tons of "devel packages")
- Possibility to generate binaries or static binaries
- Possibility to generate Linux packages (.deb, .rpm, tar.gz)
- Possibility to generate "InfluxDB docker container" (based on ubuntu)

## Getting Started
This set of tools is optimized to run on ubuntu 16.04 (ppc64le) with docker installed.

```
./influxdb_builder.py -h
Usage: influxdb_builder.py [-d <container_name> | -p] [options]

Options:
  -h, --help            show this help message and exit
  -d DOCKER_CONTAINER_NAME, --docker=DOCKER_CONTAINER_NAME
                        Build docker container with the following name
  -p, --packages        Create packages (.deb, .rpm, .tar)
  -b GIT_BRANCH, --branch=GIT_BRANCH
                        Choose the influxdb git branch (version) to compile.
                        (stable, beta, master, 0.13 ...)

  debug:
    The following options are for debugging

    --loglevel=LOGLEVEL
                        Set logging level: CRITICAL, ERROR, WARNING, INFO,
                        DEBUG (default: INFO)
```

## Examples:

### Create InfluxDB 0.13 Linux packages (.rpm, .deb, tar.gz).

```
influxdb_builder.py -p -b 0.13
```
This will fetch InfluxDB 0.13 from git repository, compile it and generate Linux packages.


### Create InfluxDB 0.13 docker container images for ppc64le.
```
influxdb_builder.py -d docker.io/schabrolles_ppc64le:0.13 -b 0.13
```
This will fetch InfluxDB 0.13 from git repository, compile it and create a docker container images with InfluxDB 0.13 for ppc64le platform.
