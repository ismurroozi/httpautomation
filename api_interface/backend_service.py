# This will host all the api interface and control the data used for verification
# from api_interface.utilities import json_util_util as json_util
# from api_interface.utilities import mongo_db_util as mongodb
from calendar import month
import utilities.conn_util as conn_util
import utilities.json_util as json_util
from datetime import datetime, timedelta
import utilities.mongo_db_util as mongodb
import os
from pathlib import Path
from bson import ObjectId

service_name_payment = "backend_service_payment"
service_name_invoice = "backend_service_invoice"
service_name_service = "backend_service_service"
headers_user = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2Mzk5YzM3ODA1Njc1YjIyOGFkMjBhNDQiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoiY3VzdG9tZXIiLCJzZXNzaW9uSUQiOiI2Mzk5YzM3ODA1Njc1YjJmNDNkMjBhNDkiLCJkYXRlIjoiMjAyMi0xMi0xNFQxMjozNzoxMi44OTZaIiwiaWF0IjoxNjcxMDIxNDMyLCJleHAiOjE2OTY5NDE0MzJ9.Shq0sa9-qg8g7jBW1tEfevrU4NAsIcRj0mXgLnoD01E", "content-language": "en"}
headers_dealer = {
    "uae": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2MmExYTY5NTRkNDAyYzIyNjEwYjA3MmMiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoic2VydmljZVByb3ZpZGVyIiwic2Vzc2lvbklEIjoiNjM3MWY1MTNhNzJlNmI3YTVhMWU1NzIxIiwiZGF0ZSI6IjIwMjItMTEtMTRUMDc6NTg6MTEuNzM3WiIsImlhdCI6MTY2ODQxMjY5MSwiZXhwIjoxNjk0MzMyNjkxfQ.IRFM3CpJYuJQJL7AsWOakLfncNK2a-psOnPf-zk532w", "content-language": "en"},
    "ksa": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI1ZjY4ODA0MjAxMmQ3NDRlNDhlZDdlODkiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoic2VydmljZVByb3ZpZGVyIiwic2Vzc2lvbklEIjoiNjM3MzdkMThiNzA1MGUxNmFhZTM2NTQzIiwiZGF0ZSI6IjIwMjItMTEtMTVUMTE6NTA6NDguMjQ5WiIsImlhdCI6MTY2ODUxMzA0OCwiZXhwIjoxNjk0NDMzMDQ4fQ.5TES70eyb-XCLJdidcTbCbUZxUwsGIC2ko71fTsEwRU", "content-language": "en"}
    }
dealer_booking_number = {
    "uae": {"active": "ADDONS-ACTIVE","force_return": "ADDONS-FORCERETURN", "completed": "ADDONS-COMPLETED"},
    "ksa": {"active": "ADDONS-ACTIVE-KSA","force_return": "ADDONS-FORCERETURN-KSA", "completed": "ADDONS-COMPLETED-KSA"}
    }
# take payment api


def take_payment(card_type, flow_identifier, flow_used_data, test_data, assign_required_value):
    api_name = "take-payment"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path = "takePayment"
    req_structure = json_util.read_req_structure(
        service_name_payment, api_name)
    booking_status = None
    if assign_required_value:
        match flow_used_data:
            case "Booking":
                booking_status = "PENDING"
            case "Recurring":
                booking_status = "CAR_PICKED"
            case "Invoice":
                booking_status = "CAR_PICKED"
                req_structure["transactionIds"] = [121212]
                req_structure["captureTransactionId"] = "121212121212"
            case "Return":
                booking_status = "RETURN_VEHICLE_REQUESTED"
                req_structure["captureTransactionId"] = "121212121212"
                returningmetadata = {}
                returningmetadata["returnReasonByCustomer"] = "string"
                returningmetadata["returnDate"] = "2022-08-20T14:16:03.680+0000"
                req_structure["returningMetadata"] = returningmetadata

        data = mongodb.read_data(
            "invygo-test", "bookings", {"currentStatus": booking_status},"")
        match flow_identifier:
            case "Booking":
                req_structure["reserveBookingId"] = str(data[0]["_id"])
            case "Recurring":
                req_structure["recurringBookingId"] = str(data[0]["_id"])
            case "Invoice":
                req_structure["bookingId"] = str(data[0]["_id"])
            case "Return":
                req_structure["returningBookingId"] = str(data[0]["_id"])

        req_structure["amount"] = data[0]["totalPrice"]
        req_structure["currency"] = data[0]["currency"]

        if card_type == "CARD":
            req_structure["type"] = "CARD"

        _, _, data = get_cards()
        paymentinfo = {}
        paymentinfo["cardId"] = str(data["data"]["cards"][0]["_id"])
        paymentinfo["cvv"] = "100"
        if test_data != "empty_sourceid":
            paymentinfo["sourceId"] = data["data"]["cards"][0]["transactionRefNumber"]
        paymentinfo["description"] = "string"
        paymentinfo["flow"] = flow_identifier
        if test_data == "invalid_card":
            paymentinfo["cardId"] = "623d7da5a609fe64259cc555"
        if test_data == "invalid_cvv":
            paymentinfo["cvv"] = "500"
        req_structure["paymentInfo"] = paymentinfo

    req_structure = json_util.assign_value_to_req_structure(
        test_data, False, service_name_payment, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(
        service_name_payment, path, req_structure, headers_user)
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))
    return status, reason, responsedata


def add_card(test_data, assign_default_value):
    api_name = "add-card"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path = "addCard"
    req_structure = json_util.read_req_structure(
        service_name_payment, api_name)
    print(req_structure)
    req_structure = json_util.assign_value_to_req_structure(
        test_data, assign_default_value, service_name_payment, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(
        service_name_payment, path, req_structure, headers_user)
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))
    return status, reason, responsedata


def get_cards():
    print("------------------------------ \nstart of case run for API get-cards\n------------------------------ ")
    path = "getCards"
    status, reason, responsedata = conn_util.get_request(
        service_name_payment, path, headers_user, {})
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))
    return status, reason, responsedata


def add_apple_pay_card(test_data, assign_default_value):
    api_name = "add-apple-pay-card"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path = "addApplePayCard"
    req_structure = json_util.read_req_structure(
        service_name_payment, api_name)
    req_structure = json_util.assign_value_to_req_structure(
        test_data, assign_default_value, service_name_payment, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(
        service_name_payment, path, req_structure, headers_user)
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))
    return status, reason, responsedata

def report_car_issue(test_data, assign_default_value):
    api_name = "report-car-issue"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path = "reportCarIssue"
    req_structure = json_util.read_req_structure(
        service_name_service, api_name)
    req_structure = json_util.assign_value_to_req_structure(
        test_data, assign_default_value, service_name_service, api_name, req_structure)
    data_before = mongodb.read_data("invygo-test", "servicerequests", {"bookingId": ObjectId(req_structure["bookingId"])}, "")
    status, reason, responsedata = conn_util.post_request(
        service_name_service, path, req_structure, headers_user)
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))
    data_after = mongodb.read_data("invygo-test", "servicerequests", {"bookingId": ObjectId(req_structure["bookingId"])}, "")
    data_dif=len(data_after)-len(data_before)
    print(data_before)
    print(data_after)
    new_data = None
    if len(data_after)>1:
        new_data = data_after[len(data_after)-1]
        # new_data.pop("_id")
    print(new_data)
    return status, reason, responsedata, data_dif, new_data

def main():

    # get_cards()
    report_car_issue(None, True)

if __name__ == "__main__":
    main()
