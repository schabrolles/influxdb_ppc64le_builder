## v1.0 [2016-08-08]

### Release Notes

With this release, you can directly generate influxdb binaries for POWER (ppc64le).

### Features
- Compilation made in a transient docker container (avoid local host pollution with tons of "devel packages")
- Possibility to generate binaries or static binaries
- Possibility to generate Linux packages (.deb, .rpm, tar.gz)
- Possibility to generate "InfluxDB docker container" (based on ubuntu)
