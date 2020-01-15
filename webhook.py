from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from ciscosparkapi import CiscoSparkAPI, SparkApiError
import json
import os
import datetime
import pytz

bearer_token = os.environ.get("bearer_token")
room_id = os.environ.get("room_id")

if bearer_token is None or room_id is None:
    print("\nWebex Teams Authorization and roomId details must be set via environment variables using below commands on macOS or Ubuntu workstation")
    print("export bearer_token=<authorization bearer token>")
    print("export room_id=<webex teams room-id>")
    print("\nWebex Teams Authorization and roomId details must be set via environment variables using below commands on Windows workstation")
    print("set bearer_token=<authorization bearer token>")
    print("set room_id=<webex teams room-id>")
    exit()

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'cleur'
app.config['BASIC_AUTH_PASSWORD'] = 'cleur'

basic_auth = BasicAuth(app)

@app.route('/',methods=['POST'])
@basic_auth.required
def alarms():
   try:
      data = json.loads(request.data)
      print(data)
      CET = pytz.timezone('Europe/Madrid')
      
      message =  'Team, **Alarm Event** : ' + data['rule_name_display'] + ', **Message** : ' + data['message'] + ', is recieved from vManage and here are the complete details<br>'
      
      temp_time = datetime.datetime.utcfromtimestamp(data['receive_time']/1000.)
      temp_time = pytz.UTC.localize(temp_time)

      message = message + '**Receive Time:** ' + temp_time.astimezone(CET).strftime('%c') + ' CET'

      temp = data['values_short_display']

      for item in temp:
          for key, value in item.items():
              message = message + '<br> **' + key + ':** ' + value

      api = CiscoSparkAPI(access_token=bearer_token)
      res=api.messages.create(roomId=room_id, markdown=message)
      print(res)
      
   except Exception as exc:
      print(exc)
      return jsonify(str(exc)), 500
   
   return jsonify("Message sent to Webex Teams"), 200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)