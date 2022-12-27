from . import mongo_db_util
import calendar
import time
from datetime import datetime

def insert_bookings_data(scenarios):
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = {}
    match scenarios:
        case "PENDING_NORMALCARD":
            query = {"currentStatus":"PENDING","customerContact":"11111111", "currency":"AED"}

    all_data= mongo_db_util.read_data("invygo-test", "bookings", query,"")
    all_data[0].pop("_id")
    all_data[0]["bookingId"]=ts
    all_data[0]["bookingDateTime"]=timenow
    all_data[0]["prefferedPaymentDate"]=timenow 
    mongo_db_util.insert_data("invygo-test", "bookings",all_data[0])
    print("Successfully inserted new bookings data, booking data: {}".format(all_data[0]))
    return ts

def delete_bookings_data(bookingId):
    mongo_db_util.remove_data("invygo-test", "bookings",{ "bookingId": bookingId })
    print("Successfully deleted bookings data, bookingid: {}".format(bookingId))

def insert_customer_cards():
    return

def delete_customer_cards():
    return

def insert_wallet_ledgers():
    return

def delete_wallet_ledgers():
    return

def main():
    bookingId = insert_bookings_data("PENDING_NORMALCARD")
    delete_bookings_data(bookingId)


if __name__ == "__main__":
    main()