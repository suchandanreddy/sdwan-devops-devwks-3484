import requests
import json

url = "http://localhost:3000/api/auth/keys"

payload =  { 
             "name": "APIkeysetup",  
             "role": "Admin"
           }

headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic YWRtaW46YWRtaW4=",
          }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

#print(response.text)

if response.status_code == 200:
    print("\nCreated API key")
else:
    exit()
    
url = "http://localhost:3000/api/datasources"

payload = {
            "name": "InfluxDB",
            "type": "influxdb",
            "access": "proxy",
            "isDefault": True,
            "password": "admin",
            "user": "admin",
            "basicAuth": True,
            "basicAuthUser": "admin",
            "basicAuthPassword": "admin",
            "jsonData": {
                            "keepCookies": []
                        },
            "secureJsonFields": {
                                    "basicAuthPassword": True
                                },
            "database": "firewall_inspect",
            "url": "http://localhost:8086",
            "readOnly": False,
            "withCredentials": False
         }


headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + api_key,
          }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

#print(response.text)


if response.status_code == 200:
    print("Added InfluxDB as a datasource")
else:
    exit()

url = "http://localhost:3000/api/dashboards/import"

payload =   {
                "dashboard": {
                    "annotations": {
                    "list": [
                        {
                        "builtIn": 1,
                        "datasource": "-- Grafana --",
                        "enable": True,
                        "hide": True,
                        "iconColor": "rgba(0, 211, 255, 1)",
                        "name": "Annotations & Alerts",
                        "type": "dashboard"
                        }
                    ]
                    },
                    "editable": True,
                    "gnetId": None,
                    "graphTooltip": 0,
                    "id": None,
                    "links": [],
                    "panels": [
                    {
                        "NonePointMode": "None",
                        "aliasColors": {},
                        "bars": False,
                        "dashLength": 10,
                        "dashes": False,
                        "datasource": "InfluxDB",
                        "fill": 1,
                        "gridPos": {
                        "h": 11,
                        "w": 24,
                        "x": 0,
                        "y": 0
                        },
                        "id": 6,
                        "legend": {
                        "avg": False,
                        "current": False,
                        "max": False,
                        "min": False,
                        "show": True,
                        "total": False,
                        "values": False
                        },
                        "lines": True,
                        "linewidth": 1,
                        "links": [],
                        "NonePointMode": "None",
                        "paceLength": 10,
                        "percentage": False,
                        "pointradius": 2,
                        "points": False,
                        "renderer": "flot",
                        "seriesOverrides": [],
                        "stack": False,
                        "steppedLine": False,
                        "targets": [
                        {
                            "groupBy": [
                            {
                                "params": [
                                "$__interval"
                                ],
                                "type": "time"
                            },
                            {
                                "params": [
                                "none"
                                ],
                                "type": "fill"
                            }
                            ],
                            "measurement": "firewall_inspect_count",
                            "orderByTime": "ASC",
                            "policy": "firewall_stats_retention_policy",
                            "refId": "A",
                            "resultFormat": "time_series",
                            "select": [
                            [
                                {
                                "params": [
                                    "value"
                                ],
                                "type": "field"
                                },
                                {
                                "params": [],
                                "type": "sum"
                                }
                            ]
                            ],
                            "tags": []
                        }
                        ],
                        "thresholds": [],
                        "timeFrom": None,
                        "timeRegions": [],
                        "timeShift": None,
                        "title": "Network view of Enterprise Firewall Inspect statistics ",
                        "tooltip": {
                        "shared": True,
                        "sort": 0,
                        "value_type": "individual"
                        },
                        "type": "graph",
                        "xaxis": {
                        "buckets": None,
                        "mode": "time",
                        "name": None,
                        "show": True,
                        "values": []
                        },
                        "yaxes": [
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        },
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        }
                        ],
                        "yaxis": {
                        "align": False,
                        "alignLevel": None
                        }
                    },
                    {
                        "NonePointMode": "None",
                        "aliasColors": {},
                        "bars": False,
                        "dashLength": 10,
                        "dashes": False,
                        "datasource": "InfluxDB",
                        "fill": 1,
                        "gridPos": {
                        "h": 8,
                        "w": 12,
                        "x": 0,
                        "y": 11
                        },
                        "id": 2,
                        "legend": {
                        "avg": False,
                        "current": False,
                        "max": False,
                        "min": False,
                        "show": True,
                        "total": False,
                        "values": False
                        },
                        "lines": True,
                        "linewidth": 1,
                        "links": [],
                        "NonePointMode": "None",
                        "paceLength": 10,
                        "percentage": False,
                        "pointradius": 5,
                        "points": False,
                        "renderer": "flot",
                        "seriesOverrides": [],
                        "spaceLength": 10,
                        "stack": False,
                        "steppedLine": False,
                        "targets": [
                        {
                            "groupBy": [
                            {
                                "params": [
                                "$__interval"
                                ],
                                "type": "time"
                            },
                            {
                                "params": [
                                "none"
                                ],
                                "type": "fill"
                            }
                            ],
                            "hide": False,
                            "measurement": "firewall_inspect_count",
                            "orderByTime": "ASC",
                            "policy": "firewall_stats_retention_policy",
                            "query": "SELECT * FROM \"firewall_inspect_count\" WHERE (\"host\" = '10.3.0.2') AND $timeFilter GROUP BY time($__interval) fill(none)",
                            "rawQuery": False,
                            "refId": "A",
                            "resultFormat": "time_series",
                            "select": [
                            [
                                {
                                "params": [
                                    "value"
                                ],
                                "type": "field"
                                },
                                {
                                "params": [],
                                "type": "first"
                                }
                            ]
                            ],
                            "tags": [
                            {
                                "key": "host",
                                "operator": "=",
                                "value": "10.3.0.1"
                            }
                            ]
                        }
                        ],
                        "thresholds": [],
                        "timeFrom": None,
                        "timeRegions": [],
                        "timeShift": None,
                        "title": "BR-cEdge-1 Router Enterprise Firewall Inspect session statistics",
                        "tooltip": {
                        "shared": True,
                        "sort": 0,
                        "value_type": "individual"
                        },
                        "type": "graph",
                        "xaxis": {
                        "buckets": None,
                        "mode": "time",
                        "name": None,
                        "show": True,
                        "values": []
                        },
                        "yaxes": [
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        },
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        }
                        ],
                        "yaxis": {
                        "align": False,
                        "alignLevel": None
                        }
                    },
                    {
                        "NonePointMode": "None",
                        "aliasColors": {},
                        "bars": False,
                        "dashLength": 10,
                        "dashes": False,
                        "datasource": "InfluxDB",
                        "fill": 1,
                        "gridPos": {
                        "h": 8,
                        "w": 12,
                        "x": 12,
                        "y": 11
                        },
                        "id": 4,
                        "legend": {
                        "avg": False,
                        "current": False,
                        "max": False,
                        "min": False,
                        "show": True,
                        "total": False,
                        "values": False
                        },
                        "lines": True,
                        "linewidth": 1,
                        "links": [],
                        "NonePointMode": "None",
                        "paceLength": 10,
                        "percentage": False,
                        "pointradius": 2,
                        "points": False,
                        "renderer": "flot",
                        "seriesOverrides": [],
                        "stack": False,
                        "steppedLine": False,
                        "targets": [
                        {
                            "groupBy": [
                            {
                                "params": [
                                "$__interval"
                                ],
                                "type": "time"
                            },
                            {
                                "params": [
                                "none"
                                ],
                                "type": "fill"
                            }
                            ],
                            "measurement": "firewall_inspect_count",
                            "orderByTime": "ASC",
                            "policy": "firewall_stats_retention_policy",
                            "refId": "A",
                            "resultFormat": "time_series",
                            "select": [
                            [
                                {
                                "params": [
                                    "value"
                                ],
                                "type": "field"
                                },
                                {
                                "params": [],
                                "type": "first"
                                }
                            ]
                            ],
                            "tags": [
                            {
                                "key": "host",
                                "operator": "=",
                                "value": "10.3.0.2"
                            }
                            ]
                        }
                        ],
                        "thresholds": [],
                        "timeFrom": None,
                        "timeRegions": [],
                        "timeShift": None,
                        "title": "BR-cEdge-2 Router Enterprise Firewall Inspect session statistics",
                        "tooltip": {
                        "shared": True,
                        "sort": 0,
                        "value_type": "individual"
                        },
                        "type": "graph",
                        "xaxis": {
                        "buckets": None,
                        "mode": "time",
                        "name": None,
                        "show": True,
                        "values": []
                        },
                        "yaxes": [
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        },
                        {
                            "format": "short",
                            "label": None,
                            "logBase": 1,
                            "max": None,
                            "min": None,
                            "show": True
                        }
                        ],
                        "yaxis": {
                        "align": False,
                        "alignLevel": None
                        }
                    }
                    ],
                    "schemaVersion": 18,
                    "style": "dark",
                    "tags": [],
                    "templating": {
                    "list": []
                    },
                    "time": {
                    "from": "now-1h",
                    "to": "now"
                    },
                    "timepicker": {
                    "refresh_intervals": [
                        "5s",
                        "10s",
                        "30s",
                        "1m",
                        "5m",
                        "15m",
                        "30m",
                        "1h",
                        "2h",
                        "1d"
                    ],
                    "time_options": [
                        "5m",
                        "15m",
                        "1h",
                        "6h",
                        "12h",
                        "24h",
                        "2d",
                        "7d",
                        "30d"
                    ]
                    },
                    "timezone": "",
                    "title": "vManage Dashboards",
                    "uid": "1v5rSKYWk",
                    "version": 3
                },
                "overwrite": True,
                "inputs": [],
                "folderId": 0
                }

headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + api_key,
          }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

#print(response.text)

if response.status_code == 200:
    print("Added vManage dashboards")
    #print(response.json())
else:
    exit()