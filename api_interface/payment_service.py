# This will host all the api interface and control the data used for verification
import utilities.conn_util as conn_util
import utilities.json_util as json_util

service_name="payment_service"

# get call http
def get_payments(provider,payment_id):
    print("------------------------------ \nstart of case run for API get-payments\n------------------------------ ")
    path = "{}/{}".format(provider,payment_id)
    status, reason, responsedata = conn_util.get_request(service_name,path,{},{})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

# /api/v1/payments/Checkout/add-card
def add_card(provider,test_data, assign_default_value):
    api_name="add-card"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="{}/{}".format(provider,api_name)
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def authorize_amount(provider,test_data, assign_default_value):
    api_name="authorize-amount"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="{}/{}".format(provider,api_name)
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def capture_amount(provider,test_data, assign_default_value):
    api_name="capture-amount"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="{}/{}".format(provider,api_name)
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def refund_amount(provider,test_data, assign_default_value):
    api_name="refund-amount"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="{}/{}".format(provider,api_name)
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def void_amount(provider,test_data, assign_default_value):
    api_name="void-amount"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="v1/{}/{}".format(provider,api_name)
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def add_apple_pay_card(provider,test_data, assign_default_value):
    api_name="add-apple-pay-card"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="v1/{}/{}".format(provider,api_name)
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def capture_apple_pay(provider,test_data, assign_default_value):
    api_name="capture-apple-pay"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="v1/{}/{}".format(provider,api_name)
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def capture_apple_pay_mada_upcoming(provider,test_data, assign_default_value):
    api_name="capture-apple-pay-mada-upcoming"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="v1/{}/{}".format(provider,api_name)
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def capture_apple_pay_outstanding(provider,test_data, assign_default_value):
    api_name="capture-apple-pay-outstanding"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="v1/{}/{}".format(provider,api_name)
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

# def main():
#     # get_payments("Tabby","a9de1573-04a3-4b27-8d28-82094d81fd3b")
#     add_card("checkout",None, True)
#     # authorize_amount("Checkout",None, False)
#     # capture_amount("Checkout",None, False)
#     # refund_amount("Checkout",None, False)
#     # void_amount("Checkout",None, False)
#     # add_apple_pay_card("Checkout",None, False)
#     # capture_apple_pay("Checkout",None, False)
#     # capture_apple_pay_mada_upcoming("Checkout",None, False)
#     # capture_apple_pay_outstanding("Checkout",None, False)

# if __name__ == "__main__":
#     main()