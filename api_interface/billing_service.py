# This will host all the api interface and control the data used for verification
from calendar import month
import utilities.conn_util as conn_util
import utilities.conn_util_v2 as conn_util_v2
import utilities.json_util as json_util
import utilities.mongo_db_util as mongodb
import utilities.data_prep as data_prep
import utilities.downstream_util as downstream_util
import backend_service
import utilities.mysql_db_util as mysqldb
from bson import ObjectId
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import requests


service_name="billing_service"
service_name_trigger_ar="billing_service_trigger_cronjob"

# take payment api
def add_card(test_data, assign_default_value):
    api_name="add-card"
    headers_add_card = {'Content-Type': 'application/json'}
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata =conn_util_v2.send_request("POST",service_name,api_name,req_structure,True, None,headers_add_card)
    redirect_link_status = 0
    if status == 200:
        response = requests.request("GET", responsedata["redirectUrl"])
        redirect_link_status = response.status_code
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata, redirect_link_status

def accept_booking(assign_default_value, scenarios_bookings_data):

    # data prep
    bookingId = data_prep.insert_bookings_data(scenarios_bookings_data)
    query = {"bookingId":bookingId}
    data_before_api = mongodb.read_data("invygo-test", "bookings", query,"")
    new_booking_data_before_api = data_before_api[0]


    request_payload = {"bookingId":str(new_booking_data_before_api["_id"]),"paymentMadeData":None}

    api_name="accept-booking"
    headers_accept_booking = {'Content-Type': 'application/json'}
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(request_payload, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata =conn_util_v2.send_request("POST",service_name,api_name,req_structure,True, None,headers_accept_booking)
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))

    time.sleep(10)
    nextPaymentDate, ar_transaction_id, ap_transaction_id, dealer_invoices_id, dealer_invoices_status, ar_clearance_id, user_invoices_id, user_invoices_status = downstream_util.get_accept_bookings_non_mada_downstream(bookingId)
    prefferedPaymentDate = datetime.strptime(new_booking_data_before_api["prefferedPaymentDate"], '%Y-%m-%d %H:%M:%S')
    difference_npd_days = (nextPaymentDate - prefferedPaymentDate).days

    # cleanup
    data_prep.delete_bookings_data(bookingId)
    return status, reason, responsedata, difference_npd_days, ar_transaction_id, ap_transaction_id, dealer_invoices_id, dealer_invoices_status, ar_clearance_id, user_invoices_id, user_invoices_status

def authorize_amount(flow_identifier, flow_used_data, test_data, assign_required_value, assign_default_value):
    api_name="authorize-amount"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="authorizeAmount"
    req_structure=json_util.read_req_structure(service_name, api_name)

    if assign_required_value:
        match flow_identifier:
            case "Booking":
                req_structure["reserveBookingId"]= "63749626b7050e3d67e5a7df"
            case "Invoice":
                req_structure["captureTransactionId"]=121212121212
                req_structure["transactionIds"]=[121212]
            case "Return":
                req_structure["captureTransactionId"]=121212121212
                req_structure["returnDate"]= "2022-08-20T14:16:03.680Z"
                req_structure["returningBookingId"]= "61bee5ecb269607beba990b0"
                req_structure["returnReasonByCustomer"]= "string"

        booking_status = None
        if assign_required_value:
            match flow_used_data:
                case "Booking":
                    booking_status = "PENDING"
                case "Invoice":
                    booking_status = "CAR_PICKED"
                case "Return":
                    booking_status = "RETURN_VEHICLE_REQUESTED"
        
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

        _,_,data = backend_service.get_cards()
        req_structure["cardId"] = str(data["data"]["cards"][0]["_id"])
        req_structure["cvv"] = "100"
        req_structure["sourceId"] = data["data"]["cards"][0]["transactionRefNumber"]
        req_structure["description"] = "string"
        req_structure["flow"] = flow_identifier

        if test_data != "empty_sourceid":
            req_structure["sourceId"] = ""
        if test_data == "invalid_card":
            req_structure["cardId"] = "623d7da5a609fe64259cc555"
        if test_data == "invalid_cvv":
            req_structure["cvv"] = "500"

    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def refund_amount(test_data, assign_default_value):
    api_name="refund-amount"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="refundAmount"
    req_structure=json_util.read_req_structure(service_name, api_name)
    req_structure=json_util.assign_value_to_req_structure(test_data, assign_default_value, service_name, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    return status, reason, responsedata

def ar_creation_for_booking(npd_scenario, invoice_scenario, invoice_created):
    api_name="ar-creation-for-booking"
    print("------------------------------ \nstart of case run for API {}\n------------------------------".format(api_name))
    path="arCreationForBooking"
    req_structure=json_util.read_req_structure(service_name_trigger_ar, api_name)
    print(req_structure)
    bookingid = ar_creation_scenarios(npd_scenario, invoice_scenario)
    test_data = {"bookingId":bookingid}
    req_structure=json_util.assign_value_to_req_structure(test_data, False, service_name_trigger_ar, api_name, req_structure)
    status, reason, responsedata = conn_util.post_request(service_name_trigger_ar,path,req_structure, {})
    print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    if invoice_created:
        print("Send duplicate request")
        status, reason, responsedata = conn_util.post_request(service_name_trigger_ar,path,req_structure, {})
        print("Status: {} and reason: {} and resp data: {}".format(status, reason, responsedata))
    
    query="SELECT * FROM account_receivables WHERE created_user IN ('AR_GENERATOR_CRON') AND booking_id IN ('{}')".format(bookingid)
    data_list = mysqldb.read_data("invygo-invoice-test", query)
    startdate=[]
    enddate=[]

    for data in data_list:
        date_hold = data[12]
        startdate.append(date_hold.strftime('%Y-%m'))
        date_hold = data[13]
        enddate.append(date_hold.strftime('%Y-%m'))

    print("startdate",startdate)
    print("enddate",enddate)

    expected_last_startdate=""
    expected_last_enddate=""
    next_month_year=(datetime.now()+relativedelta(months=+1)).strftime('%Y-%m')
    match npd_scenario:
        case "NPD_TOMORROW":
            bookingdata  = mongodb.read_data("invygo-test", "bookings", {"_id": ObjectId(bookingid)}, "")
            expected_last_startdate = (bookingdata[0]["nextPaymentDate"]).strftime('%Y-%m')
            expected_last_enddate = (bookingdata[0]["nextPaymentDate"]+ timedelta(days=29)).strftime('%Y-%m')
        case "NPD_FUTURE":
            expected_last_startdate = (data_list[0][12] + relativedelta(months=+(len(data_list)-1))).strftime('%Y-%m')
            expected_last_enddate = (data_list[0][13] + relativedelta(months=+(len(data_list)-1))).strftime('%Y-%m')
        case "NPD_PAST":
            if invoice_scenario == "INVOICE_UNPAID":
                expected_last_startdate = (data_list[0][12] + relativedelta(months=+(len(data_list)-1))).strftime('%Y-%m')
                expected_last_enddate = (data_list[0][13] + relativedelta(months=+(len(data_list)-1))).strftime('%Y-%m')
            if invoice_scenario == "INVOICE_PAID":
                bookingdata  = mongodb.read_data("invygo-test", "bookings", {"_id": ObjectId(bookingid)}, "")
                expected_last_startdate = (bookingdata[0]["nextPaymentDate"]).strftime('%Y-%m')
                expected_last_enddate = (bookingdata[0]["nextPaymentDate"]+ timedelta(days=29)).strftime('%Y-%m')

    return startdate, enddate, expected_last_startdate, expected_last_enddate, next_month_year

def ar_creation_scenarios(npd_scenario, invoice_scenario):
    bookingid = ""
    transaction_number = ""
    match invoice_scenario:
        case "INVOICE_PAID":
            bookingid = "637b2090a48ba748262eb771"
            transaction_number = 'B0000041354-M003'
        case "INVOICE_UNPAID":
            bookingid = "637b578c9d259886dc880410"
            transaction_number = 'B0000041355-M003'
        
    query="DELETE from account_receivables WHERE transaction_number NOT IN (%s) AND booking_id IN (%s) AND created_user IN (%s)"
    mysqldb.write_data_with_commit("invygo-invoice-test", query, [(transaction_number,bookingid,'AR_GENERATOR_CRON')])
    query="SELECT * FROM account_receivables WHERE transaction_name IN ('RECURRING') AND ((booking_id IN ('{}')))".format(bookingid)
    data = mysqldb.read_data("invygo-invoice-test", query)
    print(data)

    currentDateAndTime = datetime.now()
    match npd_scenario:
        case "NPD_TOMORROW":
            npd = currentDateAndTime + timedelta(days=1)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(bookingid)}, {"$set": {"nextPaymentDate": npd}})
        case "NPD_FUTURE":
            npd = currentDateAndTime + timedelta(days=10)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(bookingid)}, {"$set": {"nextPaymentDate": npd}})
        case "NPD_PAST":
            npd = currentDateAndTime - timedelta(days=4)
            mongodb.update_data("invygo-test", "bookings", {"_id": ObjectId(bookingid)}, {"$set": {"nextPaymentDate": npd}})

    return bookingid

def main():
    # add_card(None, True)
    # bookingId = data_prep.insert_bookings_data()
    # query = {"bookingId":bookingId}
    # alldata = mongodb.read_data("invygo-test", "bookings", query,"")
    # print(alldata[0]["_id"])
    status, reason, responsedata, new_booking_data_before_api = accept_booking(True,"PENDING_NORMALCARD")
    print(new_booking_data_before_api)
    # data_prep.delete_bookings_data(bookingId)
    # refund_amount(None, True)
    # authorize_amount("Booking", "Booking", None, True, True)
    # ar_creation_for_booking("NPD_PAST","INVOICE_UNPAID", False)

if __name__ == "__main__":
    main()