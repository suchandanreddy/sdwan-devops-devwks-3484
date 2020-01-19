import requests
import json
import sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = "198.18.1.10"
vmanage_port = "443"
vmanage_username = "admin"
vmanage_password = "admin"
device_template_name = "DC-vEdges"
podname = sys.argv[1]

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
            headers = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
        else:
            headers = {'Content-Type': "application/json",'Cookie': jsessionid}

        api_url = "template/device"
        base_url = "https://%s:%s/dataservice/"%(vmanage_host, vmanage_port)

        url = base_url + api_url        
        template_id_response = requests.get(url=url, headers=headers, verify=False)
        device_info = dict()

        if template_id_response.status_code == 200:
            items = template_id_response.json()['data']
            template_found=0
            print("\nFetching Template uuid of %s"%device_template_name)
            for item in items:
                if item['templateName'] == device_template_name:
                    device_info["device_template_id"] = item['templateId']
                    device_info["device_type"] = item["deviceType"]
                    template_found=1
            if template_found==0:              
                print("\nDevice Template is not found")
                exit()
        else:
            print("\nDevice Template is not found " + str(template_id_response.text))
            print("\nError fetching list of templates")
            exit()

        api_url = "template/device/config/attached/%s"%device_info["device_template_id"]
        url = base_url + api_url

        device_ids = requests.get(url=url,headers=headers,verify=False)

        if device_ids.status_code == 200:
            items = device_ids.json()['data']
            device_uuids = list()
            for i in range(len(items)):
                device_uuids.append(items[i]['uuid'])
        else:
            print("\nError retrieving attached devices" + str(device_ids.text) )
            exit()
        device_template_id = device_info["device_template_id"]

        # Fetching Device csv values

        print("\nFetching device csv values")

        payload = { 
                    "templateId":device_template_id,
                    "deviceIds":device_uuids,
                    "isEdited":False,
                    "isMasterEdited":False
                  }
        payload = json.dumps(payload)
        
        api = "template/device/config/input/"
        url = base_url + api
        device_csv_res = requests.post(url=url, data=payload,headers=headers, verify=False)

        if device_csv_res.status_code == 200:
            device_csv_values = device_csv_res.json()['data']
        else:
            print("\nError getting device csv values " + str(device_csv_res.status_code) + str(device_csv_res.text) )
            exit()

        # Adding the values to device specific variables

        host_parameters = list()

        temp_host = {
                        "device_sys_ip":"10.1.0.1",
                        "hostname":"DC1-VEDGE1-"+podname
                    }

        host_parameters.append(temp_host)

        temp = device_csv_values

        for item1 in temp:
            sys_ip = item1["csv-deviceIP"]
            for item2 in host_parameters:
                if sys_ip == item2["device_sys_ip"]:
                    item1["//system/host-name"] = item2["hostname"]             
                    break
                else:
                    continue

        device_csv_values = temp

        # Updating Device CSV values

        print("\nUpdating Device CSV values")


        payload = { 
                    "deviceTemplateList":[
                    {
                        "templateId":device_template_id,
                        "device":device_csv_values,
                        "isEdited":False,
                        "isMasterEdited":False
                    }]
                  }
        payload = json.dumps(payload)

        api = "template/device/config/attachfeature"
        url = base_url + api
        attach_template_res = requests.post(url=url, data=payload,headers=headers, verify=False)


        if attach_template_res.status_code == 200:
            attach_template_pushid = attach_template_res.json()['id']
        else:
            print("\nUpdating Device CSV values failed"+str(attach_template_res.text))
            exit()

        # Fetch the status of template push

        api = "device/action/status/%s"%attach_template_pushid
        url = base_url + api        

        while(1):
            template_status_res = requests.get(url,headers=headers,verify=False)
            if template_status_res.status_code == 200:
                if template_status_res.json()['summary']['status'] == "done":
                    print("\nUpdated Hostname")
                    break
            else:
                print("\nUpdating Hostname failed" + str(template_status_res.text))
    
    except Exception as e:
        print(e)
