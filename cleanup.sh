#!/bin/bash

docker stop grafana-influxdb_container

docker rm grafana-influxdb_container

sudo source venv/bin/activate

jupyter notebook stop

sudo python3 cleanup-webhooks.py

/opt/cisco/anyconnect/bin/vpn disconnect dcloud-rtp-anyconnect.cisco.com