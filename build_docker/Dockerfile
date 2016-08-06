FROM docker.io/schabrolles/ubuntu_ppc64le:16.04

#ENV INFLUXDB_VERSION 0.13.0
ENV DEBIAN_FRONTEND=noninteractive

COPY influxdb-static_ppc64le.tar.gz /

RUN tar zxvf influxdb-static_ppc64le.tar.gz -C /usr/bin && \
rm -rf /*.tar.gz*

COPY influxdb.conf /etc/influxdb/influxdb.conf

EXPOSE 8083 8086

VOLUME /var/lib/influxdb

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["influxd"]
