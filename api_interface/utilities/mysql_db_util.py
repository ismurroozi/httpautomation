# This space is used to host all the db utilities
from types import NoneType
import mysql.connector
from . import json_util

def new_db_conn(database):
    try:
        config = json_util.load_config()
        print(config["mysql_db"]["host"], config["mysql_db"]["username"], config["mysql_db"]["password"])
        db_conn = mysql.connector.connect(host=config["mysql_db"]["host"], username=config["mysql_db"]["username"], password=config["mysql_db"]["password"], database=database)
    except mysql.connector.Error as err:
        print(err)
        print(
            "getting db connection failed, wrong host or username or password or database")
        return
    return db_conn


def write_data_with_commit(database, query, data):
    # query = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    # OR
    # query = "UPDATE customers SET address = %s WHERE address = %s"
    # OR
    # query = "DELETE FROM customers WHERE address = %s"
    # sample data structure used for write action
    # data = [
    #     ('Peter', 'Lowstreet 4'),
    #     ('Viola', 'Sideway 1633')
    # ]

    db_conn = new_db_conn(database)
    if db_conn == NoneType:
        print("no connection available")
        return
    db_cursor = db_conn.cursor()

    try:
        print(query, data)
        if data == []:
            db_cursor.execute(query)
        else:
            db_cursor.executemany(query, data)
    except:
        db_conn.rollback()
        print("data writing failed, fallback triggered, no data being updated")
        return

    db_conn.commit()
    print(db_cursor.rowcount, "record updated.")
    db_cursor.close()
    db_conn.close()


def read_data(database, query):
    # query = "SELECT * FROM customers WHERE address ='Park Lane 38'"
    db_conn = new_db_conn(database)
    if db_conn == NoneType:
        print("no connection available")
        return
    db_cursor = db_conn.cursor()
    db_cursor.execute(query)
    data_fetch=db_cursor.fetchall()

    db_cursor.close()
    db_conn.close()
    return data_fetch


def main():
    # db=new_db_conn("invygo-invoice-test")
    # print(db)
    # db.close()

    # query="SELECT * FROM account_receivables WHERE transaction_name IN ('RECURRING') AND ((booking_id IN ('637b159da48ba72d512ea7bb')))"
    # print("sssssss",query)
    # data = read_data("invygo-invoice-test", query)
    # print(data)
    # print(len(data))
    # query="DELETE from account_receivables WHERE transaction_number NOT IN (%s) AND booking_id IN (%s) AND created_user IN (%s)"
    # print("sssssss",query)
    # write_data_with_commit("invygo-invoice-test", query, [('B0000041355-M003','637b578c9d259886dc880410','AR_GENERATOR_CRON')])
    query="SELECT * FROM wallet_ledger WHERE customer_id IN ('63623f7e7a1af74b37237fc2')"
    data = read_data("invygo-invoice-test", query)
    print(data)
    query="UPDATE wallet_ledger SET amount = 0 WHERE customer_id = '63623f7e7a1af74b37237fc2'"
    write_data_with_commit("invygo-invoice-test", query, [])

if __name__ == "__main__":
    main()
