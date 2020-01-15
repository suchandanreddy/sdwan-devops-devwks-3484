#!/bin/bash

docker stop grafana-influxdb_container

docker rm grafana-influxdb_container

source venv/bin/activate

jupyter notebook stop

python3 cleanup-webhooks.py

/opt/cisco/anyconnect/bin/vpn disconnect dcloud-rtp-anyconnect.cisco.com