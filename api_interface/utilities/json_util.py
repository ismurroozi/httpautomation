
from distutils.log import error
from errno import errorcode
import json
from msilib.schema import Error
from pathlib import Path
import csv
from datetime import datetime
from typing import Mapping


def decode_resp_data(respdata: str):
    try:
        respdata = json.loads(respdata)
        print("Successfully decode response data")
    except:
        print("json decoding failed")
    return respdata


def read_req_structure(service_name, api_name):
    json_object = None
    try:
        path = str(Path.home(
        ))+"\\automation_framework\\api_interface\\api_structure\\"+load_config()[service_name]["api_structure"]
        json_file = open(path, "r")
        json_object = json.load(json_file)[api_name]
        json_file.close()
        print("Config retrieved for service", service_name, api_name)
    except:
        print("Failed loading API structure", service_name, api_name)
    return json_object

def load_config():
    json_object = None
    try:
        path = str(Path.home()) + \
            "\\automation_framework\\api_interface\\utilities\\config.json"
        json_file = open(path, "r")
        json_object = json.load(json_file)
        print("Successfully loaded service config")
        json_file.close()
    except:
        print("Failed loading service config")
    return json_object

def load_config_v2():
    json_object = None
    try:
        path = str(Path.home()) + \
            "\\automation_framework\\api_interface\\utilities\\config_v2.json"
        json_file = open(path, "r")
        json_object = json.load(json_file)
        print("Successfully loaded service config")
        json_file.close()
    except:
        print("Failed loading service config")
    return json_object


def assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure):
    if req_structure is None:
        return req_structure
    if assign_default_value:
        req_structure = assign_default_values(service_name, api_name, req_structure)
    if test_data != None and len(test_data) > 0:
        req_structure = assign_test_values(test_data, req_structure)
    return req_structure

def assign_test_values(test_data, req_structure):
    for key_data in test_data:
        try:
            req_structure[key_data]
            req_structure[key_data] = test_data[key_data]
            print(key_data,"set to", test_data[key_data])
        except:
            print(key_data, "doesnt exist in API structure")
    print("Test data assigned successfully to API structure")
    return req_structure

def assign_default_values(service_name, api_name, req_structure):
    json_default_value = None
    try:
        path = str(Path.home(
        ))+"\\automation_framework\\api_interface\\api_structure\\"+load_config()[service_name]["sample_api_structure"]
        json_file = open(path, "r")
        json_default_value = json.load(json_file)[api_name]
        json_file.close()
        print("Successfully loaded API default value", service_name, api_name)
    except:
        print("Failed loading API default value",service_name,api_name)
        return req_structure

    for key in json_default_value:
        try:
            req_structure[key]
            req_structure[key] = json_default_value[key]
        except:
            print(key, "doesnt exist in API structure")
    print("Default value assigned for service",service_name, api_name)
    return req_structure

def modify_file(file_path, new_data: Mapping): #rowno:[trip_date:xxxx, trip_time:xxxx],rowno:[trip_date:xxxx, trip_time:xxxx]
    openfile = open(file_path,'rt')

    data = csv.DictReader(openfile)
    hold = []
    print(new_data)
    for index, row in enumerate(data):
        newdata=None
        if index in new_data:
            newdata= new_data[index]
            for new_data_key in newdata:
                row[new_data_key]=newdata[new_data_key]
        hold.append(row)

    openfile.close()


    with open(file_path,'wt',newline='')as nf:
        writer = csv.DictWriter(nf, fieldnames=data.fieldnames)
        writer.writeheader()
        writer.writerows(hold)
    
    print("successfully modified file in", file_path)

def main():
    currentDateAndTime = datetime.now()
    # new_data={
    #     0:{
    #         "Trip_Date":str(currentDateAndTime.strftime("%d/%m/%Y")),
    #         "Trip_Time":str(currentDateAndTime.strftime("%H:%M:%S")),
    #         "Tax_Invoice_No":str(currentDateAndTime.timestamp())
    #     }
    # }
    # modify_file("C:\\Users\\ismurroozi\\salik-format.csv", new_data)
    print(currentDateAndTime)

if __name__ == "__main__":
    main()
