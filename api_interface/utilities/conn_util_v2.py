import requests
from . import json_util
import json

def send_request(method,service_name,api_end_point,payload_data,is_json,files,headers):
    print("start sending request process for method {}, service {}, api {}".format(method, service_name,api_end_point))
    complete_url = get_complete_url(service_name,api_end_point)
    if is_json:
        payload=json.dumps(payload_data)
    else:
        payload=payload_data
    
    # headers = {
    #     'content-language': 'en',
    #     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2Mzk5YzM3ODA1Njc1YjIyOGFkMjBhNDQiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoiY3VzdG9tZXIiLCJzZXNzaW9uSUQiOiI2Mzk5YzM3ODA1Njc1YjJmNDNkMjBhNDkiLCJkYXRlIjoiMjAyMi0xMi0xNFQxMjozNzoxMi44OTZaIiwiaWF0IjoxNjcxMDIxNDMyLCJleHAiOjE2OTY5NDE0MzJ9.Shq0sa9-qg8g7jBW1tEfevrU4NAsIcRj0mXgLnoD01E'
    # }
    
    responsedata = requests.request(method, complete_url, headers=headers, data=payload, files=files)

    print(responsedata.text)
    print("Successfully sent method: {} || complete_path: {} || send_body: {} || send_headers: {}".format(method, complete_url, payload, headers))

    return responsedata.status_code,responsedata.reason,responsedata.json()

def get_complete_url(service_name, api_end_point):
    config = json_util.load_config_v2()
    complete_url= config[service_name]["connection_config"]["host"]+config[service_name]["connection_config"]["path"]+config[service_name][api_end_point]["end_point"]
    print("successfully construct complete url: {}".format(complete_url))
    return complete_url

def main():
    payload_data={'vehicleId': '6245aca19c1c82a7c20b568e',
    'bookingDateTime': '2022-09-11T09:00:00.000Z',
    'bookingType': '2',
    'delivery': 'true',
    'selectedMileage': '2500',
    'fullInsurance': 'false',
    'bookingPeriod': '9',
    'version': '2',
    'needAdditionalDriver': 'false'}
    files=[
        ('signatureImage',('tree.jpeg',open('C:/Users/ismurroozi/automation_framework/api_interface/utilities/template_files/tree.jpeg','rb'),'image/jpeg'))
    ]
    send_request("POST","backend_service_booking","create-booking",payload_data,False,files)

if __name__ == "__main__":
    main()