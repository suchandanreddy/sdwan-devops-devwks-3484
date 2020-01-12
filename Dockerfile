FROM ubuntu:18.04

ENV GRAFANA_VERSION 6.0.2
ENV INFLUXDB_VERSION 1.7.4

ENV DEBIAN_FRONTEND noninteractive

RUN	apt-get -y update && apt-get -y upgrade

# Install all wget supervisor and curl

RUN apt-get -y install wget supervisor curl

# Install Grafana to /src/grafana

RUN	mkdir -p src/grafana && cd src/grafana && \
		wget -nv https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana-${GRAFANA_VERSION}.linux-amd64.tar.gz -O grafana.tar.gz && \
		tar xzf grafana.tar.gz --strip-components=1 && rm grafana.tar.gz

# Install InfluxDB

RUN	wget -nv https://dl.influxdata.com/influxdb/releases/influxdb_${INFLUXDB_VERSION}_amd64.deb && \
		dpkg -i influxdb_${INFLUXDB_VERSION}_amd64.deb && rm influxdb_${INFLUXDB_VERSION}_amd64.deb

# Configure InfluxDB
ADD	influxdb/config.toml /etc/influxdb/config.toml
ADD	influxdb/run.sh /usr/local/bin/run_influxdb
ENV	PRE_CREATE_DB firewall_inspect
ENV	INFLUXDB_HOST localhost:8086
ENV	INFLUXDB_GRAFANA_USER grafana
ENV	INFLUXDB_GRAFANA_PW grafana
ENV	ROOT_PW root

# Configure Grafana
ADD ./grafana/config.ini /etc/grafana/config.ini
ADD	grafana/run.sh /usr/local/bin/run_grafana
ADD	./configure.sh /configure.sh
ADD	./set_influxdb.sh /set_influxdb.sh
RUN /configure.sh

# Configure supervisord
ADD	./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN	apt-get autoremove -y wget curl && \
		apt-get -y clean && \
		rm -rf /var/lib/apt/lists/* && rm /*.sh

# Grafana
EXPOSE	3000

# InfluxDB
EXPOSE	8086

# Run
CMD		["/usr/bin/supervisord"]