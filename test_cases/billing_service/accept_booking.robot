**** Settings ***
Library     ../../api_interface/billing_service.py
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***


*** Test Cases ***
Accept Booking Normal Card, No Promo, No Wallet
    [Tags]             HIGH
    ${status}          ${reason}                       ${responsedata}    ${difference_npd_days}    ${ar_transaction_id}    ${ap_transaction_id}    ${dealer_invoices_id}    ${dealer_invoices_status}    ${ar_clearance_id}    ${user_invoices_id}    ${user_invoices_status}=    Accept Booking    ${True}    PENDING_NORMALCARD
    Should Be Equal    ${status}                       ${200}
    Should Be Equal    ${reason}                       OK
    Should Be True     ${difference_npd_days}>${10}
    Should Be True     ${ar_transaction_id}>${0}
    Should Be True     ${ap_transaction_id}>${0}
    Should Be True     ${dealer_invoices_id}>${0}
    Should Be Equal    ${dealer_invoices_status}       PENDING
    Should Be True     ${ar_clearance_id}>${0}
    Should Be True     ${user_invoices_id}>${0}
    Should Be Equal    ${user_invoices_status}         PAID
