#!/bin/bash

while read f1 f2 f3 f4
do
        echo "Pod name     : $f1"
        Anyconnect=$f2
        Username=$f3
        Password=$f4
done < vpn_details

echo "Connecting to dcloud enivornment"

/usr/bin/expect << EOF
spawn /opt/cisco/anyconnect/bin/vpn connect $Anyconnect
expect {
    "Username:*" {
    	sleep 1
        send "$Username\r"
        exp_continue
    }
    "Password:" {
    	sleep 1
        send "$Password\r"
        exp_continue
    }
    "accept?" {
    	sleep 1
        send "y\r"
        exp_continue
    }
}
EOF

echo "Press ENTER when connected"
echo ""
read CONFIRM
echo ""

echo "Please connect to your RDP using the pod info."
echo "Press ENTER when connected"
open /Applications/Microsoft\ Remote\ Desktop.app dcloud-sevt.rdp
echo ""
read CONFIRM
echo ""

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

open "https://198.18.1.10/"

open "https://github.com/suchandanreddy/sdwan-webhooks"