# This will host all the api interface and control the data used for verification
import utilities.conn_util as conn_util
import utilities.json_util as json_util
import utilities.mongo_db_util as mongodb
import utilities.mysql_db_util as mysqldb
import backend_service
from bson import ObjectId
from datetime import datetime, timedelta

service_name = "backend_service_booking"
headers_user = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2Mzk5YzM3ODA1Njc1YjIyOGFkMjBhNDQiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoiY3VzdG9tZXIiLCJzZXNzaW9uSUQiOiI2Mzk5YzM3ODA1Njc1YjJmNDNkMjBhNDkiLCJkYXRlIjoiMjAyMi0xMi0xNFQxMjozNzoxMi44OTZaIiwiaWF0IjoxNjcxMDIxNDMyLCJleHAiOjE2OTY5NDE0MzJ9.Shq0sa9-qg8g7jBW1tEfevrU4NAsIcRj0mXgLnoD01E", "content-language": "en"}


# take payment api
def calculate_booking_cost_structure(params, swap_scenarios, wallet_scenarios):
    api_name = "calculate-booking-cost-structure"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path = "calculateBookingCostStructure"

    vehicleid = ""
    promocode = ""
    for value in params:
        if "vehicleId=" in value:
            vehicleid = value.split("vehicleId=", 1)[1]
        if "promoCode=" in value:
            promocode = value.split("promoCode=", 1)[1]
        if "swapInfo=" in value:
            params.remove(value)

    if swap_scenarios != "":
        swap_info = swap_scenarios_logic(swap_scenarios)
        params.append(swap_info)
    
    if wallet_scenarios !="":
        wallet_scenarios_logic(wallet_scenarios)

    status, reason, responsedata = conn_util.get_request(
        service_name, path, headers_user, params)
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))


    vehicle_data_db = mongodb.read_data(
        "invygo-test", "vehicles", {"_id": ObjectId(vehicleid)}, "")
    promo_data_db = mongodb.read_data(
        "invygo-test", "promotions", {"code": promocode}, "")
    query="SELECT * FROM wallet_ledger WHERE customer_id IN ('63623f7e7a1af74b37237fc2')"
    wallet_data_db = mysqldb.read_data("invygo-invoice-test", query)
    
    #reset wallet amount to 0
    if wallet_scenarios !="":
        query="UPDATE wallet_ledger SET amount = 0 WHERE customer_id = '63623f7e7a1af74b37237fc2'"
        mysqldb.write_data_with_commit("invygo-invoice-test", query, [])

    return status, reason, responsedata, vehicle_data_db, promo_data_db, wallet_data_db


def swap_scenarios_logic(swap_scenarios):
    swap_booking_id=""
    swap_date=""

    no_found_bookingid = "111111111111111111111111"
    swapped_booking_id = "636397b6aceb2e0a71995c77"
    swappable_booking_id = "638477ee9409f940f5f8419a"  # active booking
    s2o_booking_id= "6377566ba3604a2adedd142d" #active booking
    currentDateAndTime = datetime.now()

    match swap_scenarios:
        case "FIRST_MONTH_BOOKING":
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(swappable_booking_id)}, {"$set": {"bookingDateTime": currentDateAndTime}})
            swap_booking_id = swappable_booking_id
            swap_date = currentDateAndTime + timedelta(days=1)
        case "NOT_FOUND_BOOKING":
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(swappable_booking_id)}, {"$set": {"bookingDateTime": currentDateAndTime}})
            swap_booking_id = no_found_bookingid
            swap_date = currentDateAndTime + timedelta(days=1)
        case "SWAPPED_CAR":
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(swappable_booking_id)}, {"$set": {"bookingDateTime": currentDateAndTime}})
            swap_booking_id = swapped_booking_id
            swap_date = currentDateAndTime + timedelta(days=1)
        case "SWAP_40DAYS_BEFORE_NEXTPAYMENTDATE":
            bookingDateTime = currentDateAndTime - timedelta(days=120)
            nextPaymentDate = currentDateAndTime + timedelta(days=30)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(swappable_booking_id)}, {"$set": {"bookingDateTime": bookingDateTime, "nextPaymentDate": nextPaymentDate}})
            swap_booking_id = swappable_booking_id
            swap_date = currentDateAndTime - timedelta(days=15)
        case "SWAP_AFTER_RECURRING_PAYNOW+":
            bookingDateTime = currentDateAndTime - timedelta(days=120)
            nextPaymentDate = currentDateAndTime + timedelta(days=30)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(swappable_booking_id)}, {"$set": {"bookingDateTime": bookingDateTime, "nextPaymentDate": nextPaymentDate}})
            swap_booking_id = swappable_booking_id
            swap_date = currentDateAndTime + timedelta(days=10)
        case "SWAP_AFTER_RECURRING_PAYNOW0":
            bookingDateTime = currentDateAndTime - timedelta(days=120)
            nextPaymentDate = currentDateAndTime + timedelta(days=30)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(swappable_booking_id)}, {"$set": {"bookingDateTime": bookingDateTime, "nextPaymentDate": nextPaymentDate}})
            swap_booking_id = swappable_booking_id
            swap_date = currentDateAndTime + timedelta(days=5)
        case "SWAP_ONE_DAY_BEFORE_RECURRING":
            bookingDateTime = currentDateAndTime - timedelta(days=120)
            nextPaymentDate = currentDateAndTime + timedelta(days=30)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(swappable_booking_id)}, {"$set": {"bookingDateTime": bookingDateTime, "nextPaymentDate": nextPaymentDate}})
            swap_booking_id = swappable_booking_id
            swap_date = currentDateAndTime + timedelta(days=29)
        case "SWAP_ON_RECURRING":
            bookingDateTime = currentDateAndTime - timedelta(days=120)
            nextPaymentDate = currentDateAndTime + timedelta(days=30)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(swappable_booking_id)}, {"$set": {"bookingDateTime": bookingDateTime, "nextPaymentDate": nextPaymentDate}})
            swap_booking_id = swappable_booking_id
            swap_date = currentDateAndTime + timedelta(days=30)
        case "SWAP_AFTER_SCHEDULED_RECURRING":
            bookingDateTime = currentDateAndTime - timedelta(days=120)
            nextPaymentDate = currentDateAndTime + timedelta(days=25)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(swappable_booking_id)}, {"$set": {"bookingDateTime": bookingDateTime, "nextPaymentDate": nextPaymentDate}})
            swap_booking_id = swappable_booking_id
            swap_date = currentDateAndTime + timedelta(days=30)
        case "SWAP_S2O":
            bookingDateTime = currentDateAndTime - timedelta(days=120)
            nextPaymentDate = currentDateAndTime + timedelta(days=30)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(s2o_booking_id)}, {"$set": {"bookingDateTime": bookingDateTime, "nextPaymentDate": nextPaymentDate}})
            swap_booking_id = swappable_booking_id
            swap_date = currentDateAndTime + timedelta(days=30)
    
    info='swapInfo={{"swappedBookingId":"{}","swapDateTime":"{}"}}'.format(swap_booking_id, str(swap_date.strftime("%Y-%m-%d")))
    print(info)
    return info

def wallet_scenarios_logic(wallet_scenarios):
    match wallet_scenarios:
        case "WALLET_1000":
            query="UPDATE wallet_ledger SET amount = 1000 WHERE customer_id = '63623f7e7a1af74b37237fc2'"
            mysqldb.write_data_with_commit("invygo-invoice-test", query, [])

def cancel_booking(test_data, assign_default_value):
    api_name = "cancel-booking"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path = "cancelBooking"
    req_structure = json_util.read_req_structure(
        service_name, api_name)
    req_structure = json_util.assign_value_to_req_structure(
        test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(
        service_name, path, req_structure, headers_user)
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))
    return status, reason, responsedata


def main():
    # params = {"vehicleId=634cea74e77f7511e40b37d9", "selectedMileage=3000",
    #           "bookingPeriod=1", "isSwap=true"}
    # calculate_booking_cost_structure(params, "SWAP_AFTER_RECURRING_PAYNOW0", "")
    cancel_booking(None, True)


if __name__ == "__main__":
    main()
