**** Settings ***
Library     ../../api_interface/backend_service.py
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***
&{empty_payment_info}            paymentInfo={}
&{invalid_card}                  paymentInfo={cardId:6371ef94f2988e62e33ef467,cvv:100,sourceId:61a5dd550a8efdb45ee417b0,description:string,flow:Booking}
&{invalid_reserveBookingId}      reserveBookingId=121212121212121212121212
&{empty_transactionid}           transactionIds=[]
&{empty_captureTransactionId}    captureTransactionId=None
&{empty_returningMetadata}       returningMetadata={}

*** Test Cases ***
Take Payment 1 Empty Struct
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Booking    Booking    ${EMPTY}    ${False}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Take Payment 2 New Booking Success
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Booking    Booking    ${EMPTY}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 3 New Booking Use Request Returned Data
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Booking    Return    ${EMPTY}    ${False}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Take Payment 4 New Booking Use Recurring Data
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Booking    Recurring    ${EMPTY}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 5 New Booking Use Invalid Booking ID
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Booking    Booking    ${invalid_reserveBookingId}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 6 New Booking Empty Payment Info
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=               Take Payment    CARD    Booking    Booking    ${empty_payment_info}    ${True}
    Should Be Equal    ${value1}    ${500}
    Should Be Equal    ${value2}    Internal Server Error

Take Payment 7 New Booking Invalid Card
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Booking    Booking    invalid_card    ${True}
    Should Be Equal    ${value1}    ${404}
    Should Be Equal    ${value2}    Not Found

Take Payment 8 New Booking Invalid CVV
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Booking    Booking    invalid_cvv    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 9 Recurring Success
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Recurring    Recurring    ${EMPTY}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 10 Recurring Use Request Returned Data
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Recurring    Return    ${EMPTY}    ${False}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Take Payment 11 Recurring Use Booking Data
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Recurring    Booking    ${EMPTY}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 12 Recurring Use Invalid Booking ID
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Recurring    Recurring    ${invalid_reserveBookingId}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 13 Recurring Empty Payment Info
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=               Take Payment    CARD    Recurring    Recurring    ${empty_payment_info}    ${True}
    Should Be Equal    ${value1}    ${500}
    Should Be Equal    ${value2}    Internal Server Error

Take Payment 14 Recurring Invalid Card
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Recurring    Recurring    invalid_card    ${True}
    Should Be Equal    ${value1}    ${404}
    Should Be Equal    ${value2}    Not Found
    
Take Payment 15 New Booking Invalid CVV
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Recurring    Recurring    invalid_cvv    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 16 Invoice Success
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Invoice    Invoice    ${EMPTY}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 17 Invoice Use Request Returned Data
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Invoice    Return    ${EMPTY}    ${False}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Take Payment 18 Invoice Use Booking Data
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Invoice    Booking    ${EMPTY}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 19 Invoice Use Invalid Booking ID
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Invoice    Invoice    ${invalid_reserveBookingId}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 20 Invoice Empty Payment Info
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=               Take Payment    CARD    Invoice    Invoice    ${empty_payment_info}    ${True}
    Should Be Equal    ${value1}    ${500}
    Should Be Equal    ${value2}    Internal Server Error

Take Payment 21 Invoice Invalid Card
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Invoice    Invoice    invalid_card    ${True}
    Should Be Equal    ${value1}    ${404}
    Should Be Equal    ${value2}    Not Found

Take Payment 22 Invoice payment id empty
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Invoice    Invoice    ${empty_transactionid}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 23 Invoice captureTransactionId empty
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Invoice    Invoice    ${empty_captureTransactionId}    ${True}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Take Payment 24 Return Success
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Return    Return    ${EMPTY}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 25 Return Use Request Invoice Data
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Return    Invoice    ${EMPTY}    ${False}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Take Payment 26 Return Use Booking Data
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Return    Booking    ${EMPTY}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 27 Return Use Invalid Booking ID
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Return    Invoice    ${invalid_reserveBookingId}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 28 Return Empty Payment Info
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=               Take Payment    CARD    Return    Invoice    ${empty_payment_info}    ${True}
    Should Be Equal    ${value1}    ${500}
    Should Be Equal    ${value2}    Internal Server Error

Take Payment 29 Return Invalid Card
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Return    Invoice    invalid_card    ${True}
    Should Be Equal    ${value1}    ${404}
    Should Be Equal    ${value2}    Not Found

Take Payment 30 New Booking Invalid CVV
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Return    Return    invalid_cvv    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 31 Return payment id empty
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Return    Invoice    ${empty_transactionid}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 32 Return captureTransactionId empty
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Return    Invoice    ${empty_captureTransactionId}    ${True}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Take Payment 33 Return returningMetadata empty
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=    Take Payment    CARD    Return    Invoice    ${empty_returningMetadata}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Take Payment 34 New Booking Empty SourceID
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}=     Take Payment    CARD    Booking    Booking    empty_sourceid    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK