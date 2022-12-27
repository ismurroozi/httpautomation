# This will host all the api interface and control the data used for verification
import utilities.conn_util as conn_util
import utilities.json_util as json_util
import utilities.mongo_db_util as mongodb
import utilities.mysql_db_util as mysqldb
import backend_service
from bson import ObjectId
from datetime import datetime, timedelta
from pathlib import Path

service_name = "backend_service_create_booking"
headers_user = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2Mzk5YzM3ODA1Njc1YjIyOGFkMjBhNDQiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoiY3VzdG9tZXIiLCJzZXNzaW9uSUQiOiI2Mzk5YzM3ODA1Njc1YjJmNDNkMjBhNDkiLCJkYXRlIjoiMjAyMi0xMi0xNFQxMjozNzoxMi44OTZaIiwiaWF0IjoxNjcxMDIxNDMyLCJleHAiOjE2OTY5NDE0MzJ9.Shq0sa9-qg8g7jBW1tEfevrU4NAsIcRj0mXgLnoD01E", "content-language": "en"}

def create_booking(test_data, assign_default_value, parameters):
    api_name = "create-booking"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path = "createBooking"
    # req_structure = json_util.read_req_structure(
    #     service_name, api_name)
    # req_structure = json_util.assign_value_to_req_structure(
    #     test_data, assign_default_value, service_name, api_name, req_structure)
    print(parameters)
    status, reason, responsedata = conn_util.post_request(
        service_name, path, parameters, headers_user)
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))
    return status, reason, responsedata

def main():
    # params = {"vehicleId=634cea74e77f7511e40b37d9", "selectedMileage=3000",
    #           "bookingPeriod=1", "isSwap=true"}
    # calculate_booking_cost_structure(params, "SWAP_AFTER_RECURRING_PAYNOW0", "")
    text_data = { "selectedMileage": "2500", "upgradedMileage": "false",
    "vehicleId": '6245aca19c1c82a7c20b568e', "fullInsurance": "false", "bookingPeriod": "1",
    "needAdditionalDriver": "false", "delivery": "false", "bookingDateTime": "2022-12-23T05:00:00.000Z", "bookingType": "2",
    "version": "2", "starterFeeAmount": '245', "initialBookingCost": "2295", "isPaymentPending": "false", "signatureImage":""}
    filepath = str(Path.home()) + \
        json_util.load_config()["create_booking"]["signature"]
    print(filepath)
    file_data = {"signatureImage":filepath}
    parameters = {"text_data": text_data,"file_data":file_data}
    create_booking(None, True, parameters)
    print(filepath)

if __name__ == "__main__":
    main()
