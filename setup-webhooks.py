import requests
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = "198.18.1.10"
vmanage_port = "443"
vmanage_username = "admin"
vmanage_password = "admin"

requests.packages.urllib3.disable_warnings()

class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host, vmanage_port, username, password):
        api_url = "/j_security_check"
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        url = base_url + api_url
        payload = {'j_username' : username, 'j_password' : password}
        
        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            print("\nAuthentication is successful")
            return(jsessionid[0])
        except:
            print("\nAuthentication failed, No valid JSESSION ID returned")
            exit()
       
    @staticmethod
    def get_token(vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api_url = "/dataservice/client/token"
        url = base_url + api_url     
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None

if __name__ == "__main__":

    try:
        Auth = Authentication()
        jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,vmanage_username,vmanage_password)
        token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)
        
        if token is not None:
            headers = {'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
        else:
            headers = {'Cookie': jsessionid}

        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api_url = "/dataservice/settings/configuration/emailNotificationSettings"
        
        url = base_url + api_url

        settings_payload = {
                                "enabled": True,
                                "from_address": "test@test.com",
                                "protocol": "smtp",
                                "smtp_server": "test.gmail.com",
                                "smtp_port": 25,
                                "reply_to_address": "test@test.com",
                                "notification_use_smtp_authentication": False
                           }
        
        settings_response = requests.post(url=url, data=json.dumps(settings_payload), headers=headers, verify=False)

        if settings_response.status_code == 200:
            print("\nEnabled Email Notifications settings")
        else:
            print("\nFailed to enable email notifications")
            exit()
            
    except Exception as e:
        print(e)