from . import mysql_db_util, mongo_db_util

def get_account_receivables(bookingid):
    query="SELECT * FROM account_receivables WHERE booking_id IN ('{}')".format(bookingid)
    data = mysql_db_util.read_data("invygo-invoice-test", query)
    print("Successfully retreved data with query {}, data retrieved: {}".format(query, data))
    return data[0][0]

def get_account_payables(bookingid):
    query="SELECT * FROM account_payables WHERE booking_id IN ('{}')".format(bookingid)
    data = mysql_db_util.read_data("invygo-invoice-test", query)
    print("Successfully retreved data with query {}, data retrieved: {}".format(query, data))
    return data[0][0]

def get_dealer_invoice_mapping(ap_transaction_id):
    query="SELECT * FROM dealer_invoice_mapping WHERE ap_transaction_id IN ('{}')".format(ap_transaction_id)
    data = mysql_db_util.read_data("invygo-invoice-test", query)
    print("Successfully retreved data with query {}, data retrieved: {}".format(query, data))
    return data[0][1]

def get_dealer_invoices(dealer_invoice_id):
    query="SELECT * FROM dealer_invoices WHERE id IN ('{}')".format(dealer_invoice_id)
    data = mysql_db_util.read_data("invygo-invoice-test", query)
    print("Successfully retreved data with query {}, data retrieved: {}".format(query, data))
    return data[0][0], data[0][9]

def get_ar_clearance(transaction_id):
    query="SELECT * FROM ar_clearance WHERE cleared_id IN ('{}')".format(transaction_id)
    data = mysql_db_util.read_data("invygo-invoice-test", query)
    print("Successfully retreved data with query {}, data retrieved: {}".format(query, data))
    return data[0][0]

def get_invoice_transactions(transaction_id):
    query="SELECT * FROM invoice_transactions WHERE ar_transaction_id IN ('{}')".format(transaction_id)
    data = mysql_db_util.read_data("invygo-invoice-test", query)
    print("Successfully retreved data with query {}, data retrieved: {}".format(query, data))
    return data[0][0]
    
def get_invoices(invoice_id):
    query="SELECT * FROM invoices WHERE invoice_id IN ('{}')".format(invoice_id)
    data = mysql_db_util.read_data("invygo-invoice-test", query)
    print("Successfully retreved data with query {}, data retrieved: {}".format(query, data))
    return data[0][0], data[0][11]

def get_bookings(bookingId):
    query = {"bookingId":bookingId}
    data = mongo_db_util.read_data("invygo-test", "bookings", query,"")
    booking_data = data[0]
    print("Successfully retreved data with query {}, data retrieved: {}".format(query, booking_data))
    return str(booking_data["_id"]),booking_data["nextPaymentDate"]

def get_invoice_pdf(transactionId):
    query = {"transactionId":transactionId}
    data = mongo_db_util.read_data("invygo-test", "invoicepdf", query,"")
    invoice_data = data[0]
    return invoice_data["file"]

def get_accept_bookings_non_mada_downstream(bookingId):
    booking_id, nextPaymentDate = get_bookings(bookingId)
    ar_transaction_id = get_account_receivables(booking_id)
    ap_transaction_id = get_account_payables(booking_id)
    dealer_invoice_id = get_dealer_invoice_mapping(ap_transaction_id)
    dealer_invoices_id, dealer_invoices_status = get_dealer_invoices(dealer_invoice_id)
    ar_clearance_id = get_ar_clearance(ar_transaction_id)
    user_invoice_id = get_invoice_transactions(ar_transaction_id)
    user_invoices_id, user_invoices_status = get_invoices(user_invoice_id)
    
    print("Successfully retreved data related to accept booking non mada, bookings next_payment_date: {}, ar_transaction_id: {}, ap_transaction_id: {}, dealer_invoices: {}{}, ar_clearance_id: {}, user_invoices: {}{}".format(
        nextPaymentDate, ar_transaction_id, ap_transaction_id, dealer_invoices_id, dealer_invoices_status, ar_clearance_id, user_invoices_id, user_invoices_status))
    return nextPaymentDate, ar_transaction_id, ap_transaction_id, dealer_invoices_id, dealer_invoices_status, ar_clearance_id, user_invoices_id, user_invoices_status

def main():
    print(get_accept_bookings_non_mada_downstream(1672138385))

if __name__ == "__main__":
    main()