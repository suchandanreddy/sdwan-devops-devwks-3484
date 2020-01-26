#!/bin/bash

echo "Setting up Python Virtual Environment"

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt


echo "Creating docker image for ubuntu container and install InfluxDB, Grafana"

docker build -t grafana_influxdb .

docker run -d -p 3000:3000 -p 8086:8086 --name grafana-influxdb_container grafana_influxdb

echo "Starting jupyter notebook"

jupyter-notebook "notebooks/Enterprise Firewall Statistics.ipynb" &

/bin/sleep 10

open http://localhost:3000/

echo "Setting up grafana"

python3 grafana-setup.py

python3 setup-webhooks.py

python3 DCvedge-hostname-change.py $Podname

open "https://198.18.1.10/"

open "https://github.com/suchandanreddy/sdwan-devops-devwks-3484/blob/master/webhooks-guide.md"