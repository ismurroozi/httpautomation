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

service_name_payment = "backend_service_payment"
service_name_invoice = "backend_service_invoice"
headers_user = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2MzYyM2Y3ZTdhMWFmNzRiMzcyMzdmYzIiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoiY3VzdG9tZXIiLCJzZXNzaW9uSUQiOiI2MzZhMWQ3MTA1YzhmMDMwZTgzYmE2ODEiLCJkYXRlIjoiMjAyMi0xMS0wOFQwOToxMjoxNy43MjhaIiwiaWF0IjoxNjY3ODk4NzM3LCJleHAiOjE2OTM4MTg3Mzd9.x5I6vTSPEIGyrNLfgUXzUv167P8as-a7f_5CrMjq4S4", "content-language": "en"}
headers_dealer = {
    "uae": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2MmExYTY5NTRkNDAyYzIyNjEwYjA3MmMiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoic2VydmljZVByb3ZpZGVyIiwic2Vzc2lvbklEIjoiNjM3MWY1MTNhNzJlNmI3YTVhMWU1NzIxIiwiZGF0ZSI6IjIwMjItMTEtMTRUMDc6NTg6MTEuNzM3WiIsImlhdCI6MTY2ODQxMjY5MSwiZXhwIjoxNjk0MzMyNjkxfQ.IRFM3CpJYuJQJL7AsWOakLfncNK2a-psOnPf-zk532w", "content-language": "en"},
    "ksa": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI1ZjY4ODA0MjAxMmQ3NDRlNDhlZDdlODkiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoic2VydmljZVByb3ZpZGVyIiwic2Vzc2lvbklEIjoiNjM3MzdkMThiNzA1MGUxNmFhZTM2NTQzIiwiZGF0ZSI6IjIwMjItMTEtMTVUMTE6NTA6NDguMjQ5WiIsImlhdCI6MTY2ODUxMzA0OCwiZXhwIjoxNjk0NDMzMDQ4fQ.5TES70eyb-XCLJdidcTbCbUZxUwsGIC2ko71fTsEwRU", "content-language": "en"}
    }
dealer_booking_number = {
    "uae": {"active": "ADDONS-ACTIVE","force_return": "ADDONS-FORCERETURN", "completed": "ADDONS-COMPLETED"},
    "ksa": {"active": "ADDONS-ACTIVE-KSA","force_return": "ADDONS-FORCERETURN-KSA", "completed": "ADDONS-COMPLETED-KSA"}
    }


def upload_salik_fine_csv(text_data, apply_file, file_scenario):
    print("------------------------------ \nstart of case run for API upload_salik_fine_csv\n------------------------------")
    print(file_scenario)
    path = "uploadSalikFineCSV"

    filepath = str(Path.home()) + \
        json_util.load_config()["add_on_template_path"]["SALIK"]
    json_util.modify_file(filepath, salik_scenario(file_scenario))

    file_data = None
    if apply_file:
        file_data = {"csvFile": filepath}
    parameters = {"text_data": text_data, "file_data": file_data}
    status, reason, responsedata = conn_util.post_request(
        service_name_invoice, path, parameters, headers_dealer["uae"])
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))
    return status, reason, responsedata


def upload_add_on_charges_csv(text_data, apply_file, file_scenario):
    print("------------------------------ \nstart of case run for API upload_add_on_charges_csv\n------------------------------")
    print(text_data, apply_file, file_scenario)
    path = "uploadAddOnChargesCSV"
    new_file_data = {}
    try:
        addontype = text_data["addOnChargeType"]
        new_file_data = add_on_charges_scenario(file_scenario,addontype)
        if new_file_data == None:
            print("invalid add on type")
            return None, None, None
        
    except:
        print("add on charge type unknown")

    filepath = str(Path.home()) + \
        json_util.load_config()["add_on_template_path"][addontype]
    json_util.modify_file(filepath, new_file_data)

    file_data = None
    if apply_file:
        file_data = {"csvFile": filepath}
    parameters = {"text_data": text_data, "file_data": file_data}
    status, reason, responsedata = conn_util.post_request(
        service_name_invoice, path, parameters, headers_dealer[file_scenario[2]])
    print("Status: {} and reason: {} and resp data: {}".format(
        status, reason, responsedata))
    return status, reason, responsedata


def salik_scenario(file_scenario):

    new_file_data = {  # default is valid data uploaded
        0: {
            "Trip_Date": "",
            "Trip_Time": "",
            "Tax_Invoice_No": "",
            "Dealer_Booking_Number": ""
        }
    }
    within_deadline = None
    beyond_deadline = None

    match file_scenario[1]:
        case "active":
            within_deadline = datetime.now()
            beyond_deadline = within_deadline - timedelta(days=90)
            new_file_data[0]["Dealer_Booking_Number"] = dealer_booking_number["uae"]["active"]

        case "force_return":
            within_deadline = datetime.now()
            beyond_deadline = within_deadline - timedelta(days=90)
            new_file_data[0]["Dealer_Booking_Number"] = dealer_booking_number["uae"]["force_return"]

        case "completed":
            within_deadline = datetime.now()
            beyond_deadline = within_deadline - timedelta(days=90)
            new_file_data[0]["Dealer_Booking_Number"] = dealer_booking_number["uae"]["completed"]

    match file_scenario[0]:
        case "within_deadline":
            new_file_data[0]["Trip_Date"] = str(
                within_deadline.strftime("%d/%m/%Y"))
            new_file_data[0]["Trip_Time"] = str(
                within_deadline.strftime("%H:%M"))
            new_file_data[0]["Tax_Invoice_No"] = str(
                within_deadline.timestamp())
            if file_scenario[1] == "completed":
                mongodb.update_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["uae"][file_scenario[1]]}, {
                                    "$set": {"bookingCompletionDateTime": within_deadline}})

        case "beyond_deadline":
            new_file_data[0]["Trip_Date"] = str(
                beyond_deadline.strftime("%d/%m/%Y"))
            new_file_data[0]["Trip_Time"] = str(
                beyond_deadline.strftime("%H:%M"))
            new_file_data[0]["Tax_Invoice_No"] = str(
                beyond_deadline.timestamp())
            if file_scenario[1] == "completed":
                mongodb.update_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["uae"][file_scenario[1]]}, {
                                    "$set": {"bookingCompletionDateTime": beyond_deadline}})
    return new_file_data


# file_scenario:within_deadline,active,uae
def add_on_charges_scenario(file_scenario, add_on_type):
    if add_on_type == "TRAFFIC":
        new_file_data = {
            0: {
                "Date": "",
                "Time": "",
                "Tax_Invoice_No": "",
                "TF_Number": "",
                "Dealer_Booking_Number": ""
            }
        }

    elif add_on_type == "FUEL_CHARGE" or add_on_type == "DAMAGE_CHARGE" or add_on_type == "EXCEEDED_MILEAGE_CHARGE":
        new_file_data = {
            0: {
                "Date_Time": "",
                "Tax_Invoice_No": "",
                "Dealer_Booking_Number": ""
            }
        }
    else:
        return None

    
    if file_scenario[2] == "uae":
        new_file_data = add_on_charges_scenario_uae(file_scenario,add_on_type,new_file_data)
    if file_scenario[2] == "ksa":
        new_file_data = add_on_charges_scenario_ksa(file_scenario,add_on_type,new_file_data)
    return new_file_data


def add_on_charges_scenario_uae(file_scenario, add_on_type, new_file_data):
    within_deadline = None
    beyond_deadline = None
    match file_scenario[1]:
        case "active":
            within_deadline = datetime.now()
            beyond_deadline = within_deadline - timedelta(days=16)
            new_file_data[0]["Dealer_Booking_Number"] = dealer_booking_number["uae"]["active"]

        case "force_return":
            within_deadline = datetime.now()
            beyond_deadline = within_deadline - timedelta(days=16)
            new_file_data[0]["Dealer_Booking_Number"] = dealer_booking_number["uae"]["force_return"]

        case "completed":
            within_deadline = datetime.now()
            if add_on_type == "TRAFFIC" or add_on_type == "EXCEEDED_MILEAGE_CHARGE":
                beyond_deadline = within_deadline - timedelta(days=60)
            else:
                beyond_deadline = within_deadline - timedelta(days=16)
            new_file_data[0]["Dealer_Booking_Number"] = dealer_booking_number["uae"]["completed"]
    match file_scenario[0]:
        case "within_deadline":
            for struct_key in new_file_data[0]:
                if struct_key == "Date" or struct_key == "Date_Time":
                    if file_scenario[1] == "completed":
                        date_file=within_deadline - timedelta(days=1)
                        new_file_data[0][struct_key] = str(date_file.strftime("%d/%m/%Y"))
                    else:
                        new_file_data[0][struct_key] = str(within_deadline.strftime("%d/%m/%Y"))
                if struct_key == "Time":
                    new_file_data[0][struct_key] = str(
                        within_deadline.strftime("%H:%M"))
                if struct_key == "Tax_Invoice_No" or struct_key == "TF_Number":
                    new_file_data[0][struct_key] = str(
                        within_deadline.timestamp())
            if file_scenario[1] == "completed":
                mongodb.update_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["uae"][file_scenario[1]]}, {
                                    "$set": {"bookingCompletionDateTime": within_deadline}})
            elif add_on_type == "FUEL_CHARGE" or add_on_type == "DAMAGE_CHARGE" or add_on_type == "EXCEEDED_MILEAGE_CHARGE":
                try:
                    data = mongodb.read_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["uae"][file_scenario[1]]},"")
                    data1 = mongodb.read_data("invygo-test", "servicerequests", {"bookingNumber": data[0]["bookingId"]},"createdAt")
                    mongodb.update_data("invygo-test", "servicerequests", {"requestId": data1[0]["requestId"]}, {
                                        "$set": {"createdAt": within_deadline}})
                except:
                    print("db data failed to change")

        case "beyond_deadline":
            for struct_key in new_file_data[0]:
                if struct_key == "Date" or struct_key == "Date_Time":
                    new_file_data[0][struct_key] = str(
                        beyond_deadline.strftime("%d/%m/%Y"))
                if struct_key == "Time":
                    new_file_data[0][struct_key] = str(
                        beyond_deadline.strftime("%H:%M"))
                if struct_key == "Tax_Invoice_No" or struct_key == "TF_Number":
                    new_file_data[0][struct_key] = str(
                        beyond_deadline.timestamp())
            if file_scenario[1] == "completed":
                mongodb.update_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["uae"][file_scenario[1]]}, {
                                    "$set": {"bookingCompletionDateTime": beyond_deadline}})
            elif add_on_type == "FUEL_CHARGE" or add_on_type == "DAMAGE_CHARGE" or add_on_type == "EXCEEDED_MILEAGE_CHARGE":
                try:
                    data = mongodb.read_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["uae"][file_scenario[1]]},"")
                    data1 = mongodb.read_data("invygo-test", "servicerequests", {"bookingNumber": data[0]["bookingId"]},"createdAt")
                    mongodb.update_data("invygo-test", "servicerequests", {"requestId": data1[0]["requestId"]}, {
                                        "$set": {"createdAt": beyond_deadline}})
                except:
                    print("db data failed to change")
    
    return new_file_data

def add_on_charges_scenario_ksa(file_scenario, add_on_type, new_file_data):
    within_deadline = None
    beyond_deadline = None
    match file_scenario[1]:
        case "active":
            within_deadline = datetime.now()
            if add_on_type == "TRAFFIC":
                beyond_deadline = within_deadline - timedelta(days=32)
            elif add_on_type == "DAMAGE_CHARGE":
                beyond_deadline = within_deadline - timedelta(days=90)
            else:
                beyond_deadline = within_deadline - timedelta(days=90)
            new_file_data[0]["Dealer_Booking_Number"] = dealer_booking_number["ksa"]["active"]

        case "force_return":
            within_deadline = datetime.now()
            if add_on_type == "TRAFFIC":
                beyond_deadline = within_deadline - timedelta(days=60)
            elif add_on_type == "DAMAGE_CHARGE":
                beyond_deadline = within_deadline - timedelta(days=47)
            else:
                beyond_deadline = within_deadline - timedelta(days=12)
            new_file_data[0]["Dealer_Booking_Number"] = dealer_booking_number["ksa"]["force_return"]

        case "completed":
            within_deadline = datetime.now()
            if add_on_type == "TRAFFIC":
                beyond_deadline = within_deadline - timedelta(days=32)
            elif add_on_type == "DAMAGE_CHARGE":
                beyond_deadline = within_deadline - timedelta(days=47)
            else:
                beyond_deadline = within_deadline - timedelta(days=12)
            new_file_data[0]["Dealer_Booking_Number"] = dealer_booking_number["ksa"]["completed"]

    match file_scenario[0]:
        case "within_deadline":
            for struct_key in new_file_data[0]:
                if struct_key == "Date" or struct_key == "Date_Time":
                    new_file_data[0][struct_key] = str(
                        within_deadline.strftime("%d/%m/%Y"))
                if struct_key == "Time":
                    new_file_data[0][struct_key] = str(
                        within_deadline.strftime("%H:%M"))
                if struct_key == "Tax_Invoice_No" or struct_key == "TF_Number":
                    new_file_data[0][struct_key] = str(
                        within_deadline.timestamp())
            if file_scenario[1] == "completed":
                mongodb.update_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["ksa"][file_scenario[1]]}, {
                                    "$set": {"bookingCompletionDateTime": within_deadline}})
            elif add_on_type == "FUEL_CHARGE" or add_on_type == "DAMAGE_CHARGE" or add_on_type == "EXCEEDED_MILEAGE_CHARGE":
                try:
                    data = mongodb.read_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["ksa"][file_scenario[1]]},"")
                    data1 = mongodb.read_data("invygo-test", "servicerequests", {"bookingNumber": data[0]["bookingId"]},"createdAt")
                    mongodb.update_data("invygo-test", "servicerequests", {"requestId": data1[0]["requestId"]}, {
                                        "$set": {"createdAt": within_deadline}})
                except:
                    print("db data failed to change")

        case "beyond_deadline":
            for struct_key in new_file_data[0]:
                if struct_key == "Date" or struct_key == "Date_Time":
                    new_file_data[0][struct_key] = str(
                        beyond_deadline.strftime("%d/%m/%Y"))
                if struct_key == "Time":
                    new_file_data[0][struct_key] = str(
                        beyond_deadline.strftime("%H:%M"))
                if struct_key == "Tax_Invoice_No" or struct_key == "TF_Number":
                    new_file_data[0][struct_key] = str(
                        beyond_deadline.timestamp())
            if file_scenario[1] == "completed":
                mongodb.update_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["ksa"][file_scenario[1]]}, {
                                    "$set": {"bookingCompletionDateTime": beyond_deadline}})
            elif add_on_type == "FUEL_CHARGE" or add_on_type == "DAMAGE_CHARGE" or add_on_type == "EXCEEDED_MILEAGE_CHARGE":
                try:
                    data = mongodb.read_data("invygo-test", "bookings", {"dealerAgreementNumber": dealer_booking_number["ksa"][file_scenario[1]]},"")
                    data1 = mongodb.read_data("invygo-test", "servicerequests", {"bookingNumber": data[0]["bookingId"]},"createdAt")
                    mongodb.update_data("invygo-test", "servicerequests", {"requestId": data1[0]["requestId"]}, {
                                        "$set": {"createdAt": beyond_deadline}})
                except:
                    print("db data failed to change")

    return new_file_data


def main():
    # add_card(None, True)
    # _,_,data = get_cards()
    # print(data["data"]["cards"][0])
    # take_payment("CARD", "Invoice", "Invoice", {}, True)
    # upload_add_on_charges_csv(
    #     {"serviceProviderId": "5e66019d1ae30324cb9ec015", "addOnChargeType": "EXCEEDED_MILEAGE_CHARGE"}, True, ["within_deadline", "active", "ksa"])
    # upload_salik_fine_csv({"serviceProviderId":"5e3684b336feed61fe62dbe0"}, True, "beyond_deadline")
    # data = mongodb.read_data("invygo-test", "bookings", {"dealerAgreementNumber": "12345678"},"")
    # print(data[0]["bookingId"])
    # data1 = mongodb.read_data("invygo-test", "servicerequests", {"bookingNumber": data[0]["bookingId"]},"createdAt")
    # within_deadline = datetime.now()
    # mongodb.update_data("invygo-test", "servicerequests", {"requestId": data1[0]["requestId"]}, {
    #                                     "$set": {"createdAt": within_deadline}})
    data2 = mongodb.read_data("invygo-test", "servicerequests", {"bookingNumber": data[0]["bookingId"]},"createdAt")
    print(data2[0])

if __name__ == "__main__":
    main()
