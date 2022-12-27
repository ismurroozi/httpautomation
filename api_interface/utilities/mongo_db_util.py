from types import NoneType
import pymongo
from . import json_util
from datetime import datetime, timedelta
from bson import ObjectId
import calendar;
import time;


def new_db_conn():
    db_conn = None
    try:
        config = json_util.load_config()
        db_conn = pymongo.MongoClient(config["mongo_db"]["uri"])
    except:
        print(
            "getting db connection failed, wrong host or username or password or database")
        return db_conn
    return db_conn


def read_data(database, table, query, sortby):
    db_conn = new_db_conn()
    if db_conn is NoneType:
        print("no connection available")
        return
    selected_db = db_conn[database]
    selected_table = selected_db[table]
    data_fetch=None
    if sortby == "":
      data_fetch = selected_table.find(query)
    else:
      data_fetch = selected_table.find(query).sort(sortby,-1)
    print("Successfully read data in db: {}, table: {}, and with query: {}".format(database, table, query))
    datalist = list(data_fetch)
    db_conn.close()
    return datalist


def update_data(database, table, query, new_data):
    db_conn = new_db_conn()
    if db_conn is NoneType:
        print("no connection available")
        return
    selected_db = db_conn[database]
    selected_table = selected_db[table]
    selected_table.update_one(query, new_data)
    print("Successfully updated data in db: {}, table: {}, with query: {}, and new data: {}".format(database, table, query, new_data))

def insert_data(database, table, new_data):
    db_conn = new_db_conn()
    if db_conn is NoneType:
        print("no connection available")
        return
    selected_db = db_conn[database]
    selected_table = selected_db[table]
    selected_table.insert_one(new_data)
    print("Successfully inserted data to db: {}, table: {}, and new data: {}".format(database, table, new_data))

def remove_data(database, table, query):
    db_conn = new_db_conn()
    if db_conn is NoneType:
        print("no connection available")
        return
    selected_db = db_conn[database]
    selected_table = selected_db[table]
    selected_table.delete_one(query)
    print("Successfully removed data from db: {}, table: {}, and query: {}".format(database, table, query))

def main():
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    print(ts)
    all_data= read_data("invygo-test", "bookings", {"currentStatus":"PENDING","customerContact":"11111111", "currency":"AED"},"")
    print(all_data)

    all_data[0].pop("_id")
    all_data[0]["bookingId"]=ts
    print(all_data[0])
    insert_data("invygo-test", "bookings",all_data[0])
    remove_data("invygo-test", "bookings",{ "bookingId": ts })
    
    # specific_data= read_data("invygo-test", "servicerequests", {"requestId":all_data[0]["requestId"]},"")
    # print(specific_data[0]["createdAt"])
    # currentDateAndTime = datetime.now()
    # print(currentDateAndTime)
    # update_data("invygo-test", "servicerequests", {"requestId":all_data[0]["requestId"]}, {"$set": {"createdAt": currentDateAndTime }})
    # specific_data= read_data("invygo-test", "servicerequests", {"requestId":all_data[0]["requestId"]})
    # print(specific_data[0]["createdAt"])

    #  print(data[0]["totalPrice"])
    #  print(data[0]["currency"])
    # print(round(time.time() * 1000))
    #  for x in data:
    #   print(x)


if __name__ == "__main__":
    main()

# config = json_util.load_config()
# myclient = pymongo.MongoClient(config["mongo_db"]["uri"])
# mydb = myclient["invygo-test"]
# mycol = mydb["bookings"]

# myquery = {"currentStatus": "PENDING"}

# mydoc = mycol.find(myquery)

# for x in mydoc:
#     print(x)
