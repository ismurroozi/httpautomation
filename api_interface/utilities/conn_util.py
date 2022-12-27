# This space is used to host all the connection utilities
from asyncio.windows_events import NULL
from contextlib import nullcontext
import http.client
import json
from typing import Mapping
from . import json_util
import mimetypes
from codecs import encode
import urllib.parse

# VARIABLES
boundary = '----WebKitFormBoundarySOjWtBq5igiyxVqh'

# METHODS

def get_request(service_name, path, headers, params):
    # headers["Content-Type"]="application/json"
    # headers["Accept"]="application/json"
    response, responsedata = send_request(
        service_name, "GET", path, None, headers, params)
    responsedata = json_util.decode_resp_data(responsedata)
    return response.status, response.reason, responsedata


def post_request(service_name, path, parameters, headers):
    final_param=None
    print(service_name)
    print(parameters)
    if service_name in {"backend_service_invoice", "backend_service_create_booking"}:
        #FORM DATA FUNCTION
        headers["Content-Type"] = 'multipart/form-data; boundary={}'.format(boundary)
        print("aaaaaaaaaa")
        try:
            final_param=form_data(parameters)
        except:
            print("values in final param for form don't exist")
    else:
        #JSON FUNCTION
        final_param = json.dumps(parameters)
        headers["Content-Type"]="application/json"
    
    response, responsedata = send_request(
        service_name, "POST", path, final_param, headers, {})
    if response is None or responsedata is None:
        return None, None, None
    responsedata = json_util.decode_resp_data(responsedata)
    return response.status, response.reason, responsedata


def send_request(service_name, send_method: str, path: str, send_body: str, send_headers: Mapping[str, str], params):
    connection = None
    config = json_util.load_config()
    response = None
    responsedata = None

    try:
        host = config[service_name]["connection_config"]["host"]
        port = config[service_name]["connection_config"]["port"]
        complete_path = config[service_name]["connection_config"]["mapping"]+path

        if len(params) > 0:
            complete_path += "?"
            complete_path += "&".join(params)

        if host == "localhost":
            connection = http.client.HTTPConnection(host, port)
        else:
            connection = http.client.HTTPSConnection(host)
        print("Successfully connected to {}:{}".format(host, port))
        # complete_path += '?vehicleId=634cea74e77f7511e40b37d9&selectedMileage=3000&upgradedMileage=false&bookingPeriod=1&fullInsurance=false&numOfAdditionalDriver=0&isVariablePricing=false'
        connection.request(send_method, complete_path, send_body, send_headers)
        print("Successfully sent method: {} || complete_path: {} || send_body: {} || send_headers: {}".format(send_method, complete_path, send_body, send_headers))

    except:
        print("connecting failed, invalid address or method")
        return response, responsedata
    response = connection.getresponse()
    responsedata = response.read().decode()
    connection.close()
    return response, responsedata

def form_data(list_data):
    dataList = []
    print(list_data["text_data"])
    try:
        dataList+=form_text(list_data["text_data"])
    except:
        print("no data for text form")
        
    try:
        dataList+=form_file(list_data["file_data"])
    except:
        print("no data for file form")
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)

    return body

def form_text(data: Mapping[str, str]):
    dataList = []
    print("bbbbbbbbbbb")
    print(data)
    for key_data in data:
        print(key_data)
        dataList.append(encode('--' + boundary))
        dataList.append(encode("Content-Disposition: form-data; name="+key_data+";"))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(data[key_data])) 
    return dataList

def form_file(data: Mapping[str, str]):
    dataList = []
    for key_data in data:
        print(key_data)
        print(data[key_data])
        dataList.append(encode('--' + boundary))
        dataList.append(encode("Content-Disposition: form-data; name="+key_data+"; filename={0}".format(
            data[key_data])))
        fileType = mimetypes.guess_type(
            data[key_data])[0] or 'application/octet-stream'
        dataList.append(encode('Content-Type: {}'.format(fileType)))
        dataList.append(encode(''))
        with open(data[key_data], 'rb') as f:
            print(f)
            dataList.append(f.read())
    return dataList

def main():
    get_request()


if __name__ == "__main__":
    main()


